from fastapi import APIRouter, Header, Request, Depends, Body, Response
import stripe
from firebase_admin import auth
from database.firebase import db
from routers.router_auth import get_current_user
from dotenv import dotenv_values
from fastapi.responses import RedirectResponse
router = APIRouter(
    tags=["Stripe"],
    prefix='/stripe'
)

# Test de la clé API secrète
#stripe.api_key = 'sk_test_51O51rjArOje5RHk1KrKULu6bGF8jzRCFg528h3wDLBNVPotsFxPzr6IYXbUDqNH0B7unFsvkHAh7bv2byTzrrDrI00fVkfonlt'
config = dotenv_values(".env")
stripe.api_key = config['STRIPE_SK']

YOUR_DOMAIN = 'http://localhost'

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Price ID du produit à vendre
                    'price': 'price_1OA8lcArOje5RHk1qXViDkhE',
                    'quantity': 1
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        #return checkout_session
        response = RedirectResponse(url=checkout_session['url'])
        return response
    except Exception as e:
        return str(e)
    
@router.post('/webhook')
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = "whsec_79e4b26c08ab814541cc335a27bcf4ab91528a352b1c95de244660d456a70a23"
    data = await request.body()
    try: 
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data = event['data']
    except Exception as e:
        return {"error": str(e)}
    print(event_data)
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        print('Checkout session completed')
    elif event_type == 'invoice.paid':
        print('Invoice paid')
        cust_email = event_data['object']['customer_email']
        firebase_user = auth.get_user_by_email(cust_email)
        cust_id = event_data['object']['customer']
        item_id = event_data['object']['lines']['data'][0]['subscription_item']
        db.child("users").child(firebase_user.uid).child("stripe").set({"item_id": item_id, "cust_id": cust_id })
    elif event_type == 'invoice.payment_failed':
        print('Invoice payment failed')
    else:
        print(f'unhandled event: {event_type}')

    return {"status": "success"}

@router.get('/usage')
async def stripe_usage(userData: int = Depends(get_current_user)):
    fireBase_user= auth.get_user(userData['uid'])
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id = stripe_data["cust_id"]
    return stripe.Invoice.upcoming(customer=cust_id)

def increment_stripe(userId:str):
    firebase_user= auth.get_user(userId)
    stripe_data = db.child("users").child(firebase_user.uid).child("stripe").get().val()
    print(stripe_data.values())
    item_id = stripe_data['item_id']
    stripe.SubscriptionItem.create_usage_record(item_id, quantity=1)


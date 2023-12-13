// Docuemntation: https://docs.adyen.com/online-payments/build-your-integration
const clientKey = JSON.parse(document.getElementById('client-key').innerHTML);
const invoice_id = JSON.parse(document.getElementById('invoice_id').innerHTML);
const type = "dropin";

// Used to finalize a checkout call in case of redirect
const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get('sessionId'); // Unique identifier for the payment session
const redirectResult = urlParams.get('redirectResult');


// Start the Checkout workflow
async function startCheckout() {
  try {
    // Init Sessions
    const checkoutSessionResponse = await callServer("/payment/adyen/session/" + invoice_id);

    // Create AdyenCheckout using Sessions response
    const checkout = await createAdyenCheckout(checkoutSessionResponse)

    // Create an instance of Drop-in and mount it to the container you created.
    const dropinComponent = checkout.create(type).mount("#component");  // pass DIV id where component must be rendered

  } catch (error) {
    console.error(error);
    alert("Error occurred. Look at console for details");
  }
}

// Some payment methods use redirects. This is where we finalize the operation
async function finalizeCheckout() {
  try {
    // Create AdyenCheckout re-using existing Session
    const checkout = await createAdyenCheckout({id: sessionId});

    // Submit the extracted redirectResult (to trigger onPaymentCompleted(result, component) handler)
    checkout.submitDetails({details: {redirectResult}});
  } catch (error) {
    console.error(error);
    alert("Error occurred. Look at console for details");
  }
}

async function createAdyenCheckout(session) {

  const configuration = {
    clientKey,
    locale: "en_US",
    environment: "test",  // change to live for production
    showPayButton: true,
    session: session,
    paymentMethodsConfiguration: {
      ideal: {
        showImage: true
      },
      card: {
        hasHolderName: true,
        holderNameRequired: true,
        name: "Credit or debit card",
      },
      paypal: {
        environment: "test",
        countryCode: "US"   // Only needed for test. This will be automatically retrieved when you are in production.
      }
    },
    onPaymentCompleted: (result, component) => {
      handleServerResponse(result, component);
    },
    onError: (error, component) => {
      console.error(error.name, error.message, error.stack, component);
    }
  };

  return new AdyenCheckout(configuration);
}


// Calls your server endpoints
async function callServer(url, data) {
  const res = await fetch(url, {
    method: "POST",
    body: data ? JSON.stringify(data) : "",
    headers: {
      "Content-Type": "application/json"
    }
  });

  return await res.json();
}

// Handles responses sent from your server to the client
function handleServerResponse(res, component) {
  if (res.action) {
    component.handleAction(res.action);
  } else {
    switch (res.resultCode) {
      case "Authorised":
        window.location.href = "/payment/success";
      break;
      case "Pending":
      case "Received":
        window.location.href = "/payment/pending";
      break;
      case "Refused":
        window.location.href = "/payment/failed";
      break;
      default:
        window.location.href = "/payment/error";
      break;
    }
  }
}

if (!sessionId) {
  startCheckout();
}
else {
  // existing session: complete Checkout
  finalizeCheckout();
}

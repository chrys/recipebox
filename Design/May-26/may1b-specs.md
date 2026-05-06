1 Remove clerk.com functionality and use Firebase for sign up and login functionality. 
- The private key can be found at `my-recipes-8a3f9-firebase-adminsdk-fbsvc-5f8a9231f3.json`
- Use firebase script 
<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCN3Gv9ugi3mFm_hsf2R81CF6v-53t7bBg",
    authDomain: "my-recipes-8a3f9.firebaseapp.com",
    projectId: "my-recipes-8a3f9",
    storageBucket: "my-recipes-8a3f9.firebasestorage.app",
    messagingSenderId: "723385831580",
    appId: "1:723385831580:web:88987ec5601ed825fc1d59",
    measurementId: "G-3GPETSS1SB"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>

- Package firebase-admin is already installed 

- Initialize the SDK in settings.py
```
import firebase_admin
from firebase_admin import credentials

# Path to your JSON key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
```

- Create the Frontend Login/Sign-up Forms
```
<form id="auth-form">
    <input type="email" id="email" placeholder="Email" required>
    <input type="password" id="password" placeholder="Password" required>
    <button type="button" onclick="handleAuth('signup')">Sign Up</button>
    <button type="button" onclick="handleAuth('login')">Login</button>
</form>

<!-- Load Firebase SDKs -->
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-app.js";
  import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js";

  const firebaseConfig = { /* firebaseconfig */  };
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);

  window.handleAuth = async (action) => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
      let userCredential;
      if (action === 'signup') {
        userCredential = await createUserWithEmailAndPassword(auth, email, password);
      } else {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      }
      
      // Get the ID Token to send to Django
      const idToken = await userCredential.user.getIdToken();
      
      // Send token to Django via POST
      const response = await fetch('/firebase-login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ id_token: idToken })
      });

      if (response.ok) {
        window.location.href = '/dashboard/';
      }
    } catch (error) {
      alert(error.message);
    }
  };
</script>
```

- Update URLS 
```
from django.urls import path
from .views import firebase_login

urlpatterns = [
    path('firebase-login/', firebase_login, name='firebase_login'),
    # Add your other paths like dashboard, etc.
]
```


import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore/lite';

const firebaseConfig = {
  apiKey: "AIzaSyDR2kPCdpwogYLYCwU7r1StPfEgrgEXuAo",
  authDomain: "coffie-break.firebaseapp.com",
  projectId: "coffie-break",
  storageBucket: "coffie-break.appspot.com",
  messagingSenderId: "80259187116",
  appId: "1:80259187116:web:52091ac204b2c78430ba09"
};


const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default db;

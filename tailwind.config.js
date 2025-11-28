 /** @type {import('tailwindcss').Config} */
export default {
   content: [
    "./files/templates/**/*.{html,js}",
    "./files/templates/type/*.{py,html}",
    "./files/templates/*.{py,html}",
    "./files/*.py",
    // accounts
    "./accounts/templates/accounts/*.{html,js}",


   ],
   theme: {
     extend: {},
   },
   plugins: [],
 }
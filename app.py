from flask import Flask, render_template, request

app = Flask(__name__)

# بيانات المنيو مؤقتة هنا (الأسعار والأصناف للتجربة بس).
# بعدين هننقلها لقاعدة البيانات.
MENU = [
    {
        "category": "فرايد تشيكن",
        "items": [
            {"name": "وجبة كرانشي 2 قطعة", "desc": "قطعتين فراخ مقرمشة، بطاطس، كول سلو، عيش وثومية.", "price": 95, "icon": "🍗"},
            {"name": "وجبة كرانشي 4 قطع", "desc": "4 قطع فراخ مقرمشة، بطاطس، كول سلو، عيش وثومية.", "price": 160, "icon": "🍗", "popular": True},
            {"name": "بكت العيلة 8 قطع", "desc": "8 قطع فراخ مع بطاطس كبيرة وكول سلو وعيش، تكفي 3 إلى 4 أفراد.", "price": 290, "icon": "🍗"},
            {"name": "ستريبس كرانشي", "desc": "5 صوابع صدور فراخ مقرمشة مع صوص من اختيارك.", "price": 110, "icon": "🍤"},
        ],
    },
    {
        "category": "شاورما",
        "items": [
            {"name": "ساندويتش شاورما فراخ", "desc": "شاورما فراخ، ثومية، مخلل وطماطم في عيش صاج.", "price": 70, "icon": "🌯", "popular": True},
            {"name": "ساندويتش شاورما لحمة", "desc": "شاورما لحمة، طحينة، بصل بالسماق وطماطم.", "price": 95, "icon": "🌯"},
            {"name": "طبق شاورما فراخ", "desc": "شاورما فراخ على أرز أو بطاطس، مع سلطة وثومية وعيش.", "price": 125, "icon": "🍛"},
            {"name": "شاورما مكس", "desc": "نص فراخ ونص لحمة، مع بطاطس جوه الساندويتش.", "price": 110, "icon": "🌯", "popular": True},
        ],
    },
    {
        "category": "إضافات ومشروبات",
        "items": [
            {"name": "بطاطس مقلية", "desc": "حصة كبيرة، متبلة.", "price": 35, "icon": "🍟"},
            {"name": "كول سلو", "desc": "", "price": 20, "icon": "🥗"},
            {"name": "ثومية إضافية", "desc": "", "price": 10, "icon": "🧄"},
            {"name": "مشروب غازي", "desc": "", "price": 20, "icon": "🥤"},
            {"name": "ليمون بالنعناع", "desc": "عصير طازة.", "price": 30, "icon": "🍋"},
        ],
    },
]


@app.route("/")
def home():
    popular = [i for cat in MENU for i in cat["items"] if i.get("popular")]
    return render_template("index.html", popular=popular)


@app.route("/menu")
def menu():
    return render_template("menu.html", menu=MENU)


@app.route("/booking", methods=["GET", "POST"])
def booking():
    sent = None
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        if not (name and phone and date and time):
            error = "كمّل الاسم ورقم الموبايل والتاريخ والوقت عشان نقدر نأكد الحجز."
        else:
            # لسه مش بنحفظ الحجز، ده هنعمله في خطوة الداتابيز.
            sent = {"name": name, "phone": phone}
    return render_template("booking.html", sent=sent, error=error)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
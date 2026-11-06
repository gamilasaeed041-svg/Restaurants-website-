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
        "category": "النجريسكو",
        "items": [
            {"name": "نجريسكو فراخ", "desc": "", "price": 125, "icon": "🍗"},
            {"name": "نجريسكو لحمة مفرومة", "desc": "", "price": 125, "icon": "🥩"},
            {"name": "نجريسكو شاورما فراخ", "desc": "", "price": 135, "icon": "🌯"},
            {"name": "نجريسكو زينجر", "desc": "", "price": 125, "icon": "🍗"},
            {"name": "نجريسكو ميكس فراخ", "desc": "", "price": 135, "icon": "🍗"},
            {"name": "نجريسكو ميكس لحوم", "desc": "", "price": 140, "icon": "🥩"},
        ],
    },
    {
        "category": " الكريب",
        "items": [
            {"name": "كريب شاورما فراخ", "desc": "", "price": 110, "icon": "🌯"},
            {"name": "كريب ميكس فراخ", "desc": "", "price": 110, "icon": "🌯"},
            {"name": "كريب ميكس لحوم", "desc": "", "price": 120, "icon": "🌯"},
            {"name": "كريب سوبر اسباسيال", "desc": "", "price": 110, "icon": "🌯"},
            {"name": "كريب فاهيتا", "desc": "", "price": 100, "icon": "🌯"},
            {"name": "كريب بطاطس", "desc": "", "price": 70, "icon": "🌯"},
        ],
    },
    {
        "category": "فطير حادق",
        "items": [
            {"name": "فطير لحمة", "desc": "", "price": 140, "icon": "🥧"},
            {"name": "فطير لحمة مفرومة", "desc": "", "price": 140, "icon": "🥧"},
            {"name": "فطير زينجر", "desc": "", "price": 140, "icon": "🥧"},
            {"name": "فطير استريبس", "desc": "", "price": 140, "icon": "🥧"},
            {"name": "فطير كريمة بسطرمة", "desc": "", "price": 150, "icon": "🥧"},
            {"name": "فطير جبنة", "desc": "", "price": 140, "icon": "🥧"},
            {"name": "فطير ميكس لحوم", "desc": "", "price": 180, "icon": "🥧"},
            {"name": "فطير ميكس فراخ", "desc": "", "price": 150, "icon": "🥧"},
        ],
    },
    {
        "category": "فطير حلو",
        "items": [
            {"name": "فطير سكر", "desc": "", "price": 70, "icon": "🥞"},
            {"name": "فطير سكر ولبن", "desc": "", "price": 90, "icon": "🥞"},
            {"name": "فطير نوتيلا", "desc": "", "price": 100, "icon": "🥞"},
            {"name": "فطير شعبة وعسل", "desc": "", "price": 100, "icon": "🥞"},
        ],
    },
    {
        "category": "كساديلا",
        "items": [
            {"name": "كساديلا فراخ", "desc": "", "price": 150, "icon": "🌮"},
            {"name": "كساديلا استريبس", "desc": "", "price": 150, "icon": "🌮"},
        ],
    },
    {
        "category": "البيتزا",
        "items": [
            {"name": "بيتزا مارجريتا", "desc": "", "price": 120, "icon": "🍕"},
            {"name": "بيتزا سبيشيال", "desc": "", "price": 130, "icon": "🍕"},
            {"name": "بيتزا فراخ", "desc": "", "price": 130, "icon": "🍕"},
            {"name": "بيتزا باربكيو", "desc": "", "price": 140, "icon": "🍕"},
            {"name": "بيتزا رانش", "desc": "", "price": 140, "icon": "🍕"},
            {"name": "بيتزا زينجر", "desc": "", "price": 150, "icon": "🍕"},
            {"name": "بيتزا استريبس", "desc": "", "price": 150, "icon": "🍕"},
            {"name": "بيتزا ميكس لحوم", "desc": "", "price": 165, "icon": "🍕"},
        ],
    },
    {
        "category": "الوجبات",
        "items": [
            {"name": "وجبة عربي فراخ", "desc": "", "price": 140, "icon": "🍗"},
            {"name": "وجبة ماريا فراخ", "desc": "", "price": 130, "icon": "🍗"},
            {"name": "وجبة زينجر", "desc": "", "price": 170, "icon": "🍗"},
            {"name": "وجبة استريبس", "desc": "", "price": 170, "icon": "🍗"},
        ],
    },
    {
        "category": " الساندويتشات",
        "items": [
            {"name": "ساندويتش شاورما فراخ", "desc": "", "price": 100, "icon": "🥙"},
            {"name": "ساندويتش فراخ بطاطس", "desc": "", "price": 110, "icon": "🥙"},
            {"name": "ساندويتش كيزر فراخ", "desc": "", "price": 50, "icon": "🥙"},
            {"name": "ساندويتش فاهيتا", "desc": "", "price": 100, "icon": "🥙"},
            {"name": "ساندويتش استريبس", "desc": "", "price": 100, "icon": "🥙"},
            {"name": "ساندويتش زينجر", "desc": "", "price": 100, "icon": "🥙"},
            {"name": "ساندويتش بطاطس سوري", "desc": "", "price": 40, "icon": "🥙"},
        ],
    },
    {
        "category": "الفتة",
        "items": [
            {"name": "فتة فراخ", "desc": "", "price": 130, "icon": "🍗"},
            {"name": "فتة فاهيتا", "desc": "", "price": 130, "icon": "🥩"},
        ],
    },
    {
        "category": "الفرايز",
        "items": [
            {"name": "فرايز عادي", "desc": "", "price": 40, "icon": "🍟"},
            {"name": "فرايز جبنة شيدر", "desc": "", "price": 60, "icon": "🍟"},
            {"name": "فرايز اسبيشيال", "desc": "", "price": 100, "icon": "🍟"},
        ],
    },
    {
        "category": "البرجر",
        "items": [
            {"name": "برجر لحمة", "desc": "", "price": 100, "icon": "🍔"},
            {"name": "برجر فراخ", "desc": "", "price": 100, "icon": "🍔"},
            {"name": "دبل لحمة", "desc": "", "price": 150, "icon": "🍔"},
            {"name": "دبل فراخ", "desc": "", "price": 150, "icon": "🍔"},
        ],
    },
    {
        "category": "الحواوشي",
        "items": [
            {"name": "حواوشي بلدي", "desc": "", "price": 70, "icon": "🫓"},
            {"name": "حواوشي سوري", "desc": "", "price": 80, "icon": "🫓"},
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
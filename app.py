import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import datetime
import pandas as pd

st.set_page_config(
    page_title="T.C. Gümrük ve Lojistik ERP", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 5 DİLLİ TAM KUSURSUZ ÇEVİRİ VE LOKALİZASYON SÖZLÜĞÜ (KALEMLER DAHİL) ---
TRANSLATIONS = {
    "Türkçe": {
        "title": "T.C. Gümrük ve Lojistik ERP",
        "subtitle": "Gümrük Yönetmeliği Md. 114 kapsamında entegre çalışan kurumsal sevk ve operasyon merkezi.",
        "menu_dashboard": "Ana Kontrol Paneli",
        "menu_gemi": "Deniz Yolu Gemi Haritası",
        "menu_tir": "Kara Yolu Tır Filo Haritası",
        "menu_pdf": "Sevk Evraki & PDF Motoru",
        "menu_ekle": "Yeni Sevk Kaydı Ekle",
        "menu_parca_ekle": "Yeni Envanter Kalemi Ekle",
        "menu_siteler": "Resmi Dış Ticaret Portalları",
        "menu_loglar": "Sistem Logları",
        "update_btn": "Canlı Verileri ve Sistemi Güncelle",
        "total_sevk": "Aktif Sevk Sayısı",
        "active_fleet": "Aktif Taşıt Filosu",
        "system_status": "Sistem Durumu",
        "compliance": "Mevzuat Uyum",
        "table_header": "Güncel Sevk ve Konteyner Veritabanı",
        "col_sevk": "Sevk No",
        "col_alici": "Alıcı Firma",
        "col_ulke": "Ülke",
        "col_kap": "Kap",
        "col_net": "Net (Kg)",
        "col_durum": "Durum",
        "status_onayli": "Gümrük Onaylı",
        "status_seyirde": "Denizde Seyirde",
        "status_teslim": "Liman Teslimi",
        "status_gumrukte": "Gümrükte",
        "status_yol": "Yola Çıktı",
        "status_yeni": "Yeni Kayıt",
        "map_gemi_title": "Deniz Yolu Gemi Radar ve Konum Matrisi",
        "map_gemi_desc": "Uluslararası limanlar arası seyir halindeki gemilerin anlık konum bilgileri.",
        "map_tir_title": "Kara Yolu Tır Filo ve Rota Matrisi",
        "map_tir_desc": "Avrupa otoyollarında ve sınır kapılarında yük taşıyan tırların harita konumu.",
        "pdf_title": "Resmi Gümrük Onaylı PDF Motoru",
        "pdf_desc": "Gümrük mevzuatına tam uyumlu, resmi mühürlü sevk belgesi oluşturun.",
        "gemi_matrix": "Küresel Deniz Filosu Konum Matrisi",
        "tir_matrix": "Uluslararası Tır Filosu Konum Matrisi",
        "btn_gemi": "MarineTraffic Canlı Dünya Gemi Haritasını Aç ↗",
        "btn_tir": "Canlı Kara Yolu Tır Takip Haritasını Aç ↗",
        "form_sevk_no": "Sevk / Beyanname Numarası",
        "form_alici": "Alıcı Firma Resmi Ünvanı",
        "form_ulke": "Hedef Ülke",
        "form_kap": "Kap Adedi",
        "form_net": "Net Ağırlık (Kg)",
        "form_brut": "Brüt Ağırlık (Kg)",
        "form_teslim": "Incoterms Teslim Şekli",
        "form_pdf_btn": "Resmi PDF Sevk Evrakını Üret ve İndir",
        "form_ekle_btn": "Kaydı Veritabanına Ekle",
        "success_pdf": "İşlem Başarılı! Gümrük sevk evrakı hazırlandı.",
        "success_ekle": "başarıyla eklendi!",
        # Kalemler / Envanter Çevirileri
        "parca_banner_title": "➕ Yeni Envanter Kalemi ve Parça Tanımla",
        "parca_banner_desc": "Ürün kodu, parça adı, malzeme türü, ilgili üretim hattı ve başlangıç stok miktarını kaydedin.",
        "parca_kod": "Ürün Kodu",
        "parca_ad": "Parça Adı",
        "parca_malzeme": "Malzeme Türü",
        "parca_hat": "İlgili Üretim Hattı",
        "parca_stok": "Başlangıç Stok Miktarı",
        "parca_btn": "💾 Parçayı Veritabanına Kaydet",
        "parca_success": "başarıyla envantere eklendi!",
        "parca_table_header": "📋 Kayıtlı Envanter Kalemleri Veritabanı",
        "col_p_kod": "Ürün Kodu",
        "col_p_ad": "Parça Adı",
        "col_p_malzeme": "Malzeme",
        "col_p_hat": "İlgili Üretim Hattı",
        "col_p_stok": "Başlangıç Stok",
        "site_1_title": "T.C. Ticaret Bakanlığı",
        "site_1_desc": "Resmi mevzuat ve dış ticaret.",
        "site_1_btn": "Siteye Git ↗",
        "site_2_title": "E-Devlet Gümrük",
        "site_2_desc": "Beyanname işlemleri.",
        "site_2_btn": "Siteye Git ↗",
        "site_3_title": "Ulaştırma Bakanlığı",
        "site_3_desc": "Liman operasyonları.",
        "site_3_btn": "Siteye Git ↗",
        "log_title": "Sistem Logları",
        "log_desc": "Arka planda çalışan motorun durum raporu.",
        "unit_adet": "Adet",
        "unit_tasit": "Taşıt",
        "status_online": "Çevrimiçi"
    },
    "English": {
        "title": "TC Customs and Logistics ERP",
        "subtitle": "Enterprise shipment and operation center integrated under Customs Regulation Art. 114.",
        "menu_dashboard": "Main Control Panel",
        "menu_gemi": "Maritime Vessel Map",
        "menu_tir": "Road Freight Truck Map",
        "menu_pdf": "Shipping Document & PDF Engine",
        "menu_ekle": "Add New Shipment",
        "menu_parca_ekle": "Add New Inventory Item",
        "menu_siteler": "Official Trade Portals",
        "menu_loglar": "System Logs",
        "update_btn": "Refresh Live Data & System",
        "total_sevk": "Active Shipments",
        "active_fleet": "Active Fleet",
        "system_status": "System Status",
        "compliance": "Compliance",
        "table_header": "Current Shipment & Container Database",
        "col_sevk": "Shipment No",
        "col_alici": "Consignee",
        "col_ulke": "Country",
        "col_kap": "Packages",
        "col_net": "Net (Kg)",
        "col_durum": "Status",
        "status_onayli": "Customs Approved",
        "status_seyirde": "At Sea",
        "status_teslim": "Port Delivery",
        "status_gumrukte": "At Customs",
        "status_yol": "Dispatched",
        "status_yeni": "New Record",
        "map_gemi_title": "Maritime Vessel Radar & Location Matrix",
        "map_gemi_desc": "Real-time location information of vessels navigating between international ports.",
        "map_tir_title": "Road Freight Truck Fleet & Route Matrix",
        "map_tir_desc": "Map locations of trucks carrying cargo on European highways and border gates.",
        "pdf_title": "Official Customs Approved PDF Engine",
        "pdf_desc": "Generate fully compliant, officially sealed shipping documents under customs regulations.",
        "gemi_matrix": "Global Maritime Fleet Location Matrix",
        "tir_matrix": "International Truck Fleet Location Matrix",
        "btn_gemi": "Open MarineTraffic Live World Vessel Map ↗",
        "btn_tir": "Open Live Road Freight Truck Tracking Map ↗",
        "form_sevk_no": "Shipment / Declaration Number",
        "form_alici": "Official Consignee Company Title",
        "form_ulke": "Destination Country",
        "form_kap": "Package Quantity",
        "form_net": "Net Weight (Kg)",
        "form_brut": "Gross Weight (Kg)",
        "form_teslim": "Incoterms Delivery Term",
        "form_pdf_btn": "Generate & Download Official PDF Document",
        "form_ekle_btn": "Add Record to Database",
        "success_pdf": "Operation Successful! Customs shipping document prepared.",
        "success_ekle": "successfully added!",
        # Kalemler / Envanter Çevirileri
        "parca_banner_title": "➕ Add New Inventory Item & Part",
        "parca_banner_desc": "Register product code, part name, material type, related production line, and initial stock quantity.",
        "parca_kod": "Product Code",
        "parca_ad": "Part Name",
        "parca_malzeme": "Material Type",
        "parca_hat": "Related Production Line",
        "parca_stok": "Initial Stock Quantity",
        "parca_btn": "💾 Save Part to Database",
        "parca_success": "successfully added to inventory!",
        "parca_table_header": "📋 Registered Inventory Items Database",
        "col_p_kod": "Product Code",
        "col_p_ad": "Part Name",
        "col_p_malzeme": "Material",
        "col_p_hat": "Production Line",
        "col_p_stok": "Initial Stock",
        "site_1_title": "Ministry of Trade",
        "site_1_desc": "Official legislation and foreign trade.",
        "site_1_btn": "Visit Site ↗",
        "site_2_title": "E-Government Customs",
        "site_2_desc": "Declaration and cargo procedures.",
        "site_2_btn": "Visit Site ↗",
        "site_3_title": "Ministry of Transport",
        "site_3_desc": "Port operations and maritime rules.",
        "site_3_btn": "Visit Site ↗",
        "log_title": "System Logs",
        "log_desc": "Status report of the background execution engine.",
        "unit_adet": "Units",
        "unit_tasit": "Fleet",
        "status_online": "Online"
    },
    "Deutsch": {
        "title": "TC Zoll- und Logistik-ERP",
        "subtitle": "Unternehmens-Versand- und Einsatzzentrum, integriert nach Zollverordnung Art. 114.",
        "menu_dashboard": "Hauptkontrollpanel",
        "menu_gemi": "Schifffahrtskarte",
        "menu_tir": "Lkw-Flottenkarte",
        "menu_pdf": "Versanddokument & PDF-Engine",
        "menu_ekle": "Neue Sendung Hinzufügen",
        "menu_parca_ekle": "Neuen Artikel Hinzufügen",
        "menu_siteler": "Offizielle Handelsportale",
        "menu_loglar": "Systemprotokolle",
        "update_btn": "Live-Daten & System Aktualisieren",
        "total_sevk": "Aktive Sendungen",
        "active_fleet": "Aktive Flotte",
        "system_status": "Systemstatus",
        "compliance": "Konformität",
        "table_header": "Aktuelle Sendungs- und Containerdatenbank",
        "col_sevk": "Sendungs-Nr",
        "col_alici": "Empfänger",
        "col_ulke": "Land",
        "col_kap": "Pakete",
        "col_net": "Netto (Kg)",
        "col_durum": "Status",
        "status_onayli": "Zollgenehmigt",
        "status_seyirde": "Auf See",
        "status_teslim": "Hafenlieferung",
        "status_gumrukte": "Beim Zoll",
        "status_yol": "Unterwegs",
        "status_yeni": "Neuer Eintrag",
        "map_gemi_title": "Schifffahrtsradar & Standortmatrix",
        "map_gemi_desc": "Echtzeit-Standortinformationen von Schiffen auf internationaler Fahrt.",
        "map_tir_title": "Lkw-Flotten- und Routenmatrix",
        "map_tir_desc": "Standortkarte von Lkw im Frachtverkehr auf europäischen Autobahnen.",
        "pdf_title": "Offizielle Zoll-Genehmigte PDF-Engine",
        "pdf_desc": "Erstellen Sie offiziell versiegelte Versanddokumente nach Zollvorschriften.",
        "gemi_matrix": "Globale Seeschifffahrts-Standortmatrix",
        "tir_matrix": "Internationale Lkw-Flotten-Standortmatrix",
        "btn_gemi": "MarineTraffic Live-Welt-Schiffskarte Öffnen ↗",
        "btn_tir": "Live Lkw-Tracking-Karte Öffnen ↗",
        "form_sevk_no": "Sendungs- / Deklarationsnummer",
        "form_alici": "Offizieller Firmenname des Empfängers",
        "form_ulke": "Zielland",
        "form_kap": "Anzahl der Pakete",
        "form_net": "Nettogewicht (Kg)",
        "form_brut": "Bruttogewicht (Kg)",
        "form_teslim": "Incoterms Lieferbedingung",
        "form_pdf_btn": "Offizielles PDF-Dokument Erstellen & Herunterladen",
        "form_ekle_btn": "Datensatz zur Datenbank Hinzufügen",
        "success_pdf": "Vorgang erfolgreich! Zollversanddokument vorbereitet.",
        "success_ekle": "erfolgreich hinzugefügt!",
        # Kalemler / Envanter Çevirileri
        "parca_banner_title": "➕ Neuen Inventarartikel & Teil Hinzufügen",
        "parca_banner_desc": "Erfassen Sie Produktcode, Teilenamen, Materialart, zugehörige Fertigungslinie und Anfangsbestand.",
        "parca_kod": "Produktcode",
        "parca_ad": "Teilename",
        "parca_malzeme": "Materialart",
        "parca_hat": "Zugehörige Fertigungslinie",
        "parca_stok": "Anfangsbestand",
        "parca_btn": "💾 Teil in Datenbank Speichern",
        "parca_success": "erfolgreich zum Inventar hinzugefügt!",
        "parca_table_header": "📋 Datenbank der registrierten Inventarartikel",
        "col_p_kod": "Produktcode",
        "col_p_ad": "Teilename",
        "col_p_malzeme": "Material",
        "col_p_hat": "Fertigungslinie",
        "col_p_stok": "Anfangsbestand",
        "site_1_title": "Handelsministerium",
        "site_1_desc": "Offizielle Gesetzgebung und Außenhandel.",
        "site_1_btn": "Website Besuchen ↗",
        "site_2_title": "E-Government Zoll",
        "site_2_desc": "Zollanmeldungsverfahren.",
        "site_2_btn": "Website Besuchen ↗",
        "site_3_title": "Verkehrsministerium",
        "site_3_desc": "Hafenoperationen und Schifffahrt.",
        "site_3_btn": "Website Besuchen ↗",
        "log_title": "Systemprotokolle",
        "log_desc": "Statusbericht der Hintergrund-Ausführungs-Engine.",
        "unit_adet": "Stück",
        "unit_tasit": "Fahrzeuge",
        "status_online": "Online"
    },
    "Русский": {
        "title": "ERP Таможни и Логистики ТР",
        "subtitle": "Корпоративный центр отгрузок и операций в соответствии со ст. 114 Таможенного регламента.",
        "menu_dashboard": "Главная панель управления",
        "menu_gemi": "Карта морских судов",
        "menu_tir": "Карта автопарка грузовиков",
        "menu_pdf": "Документ отгрузки и PDF движок",
        "menu_ekle": "Добавить новую отгрузку",
        "menu_parca_ekle": "Добавить позицию инвентаря",
        "menu_siteler": "Официальные торговые порталы",
        "menu_loglar": "Системные логи",
        "update_btn": "Обновить данные в реальном времени",
        "total_sevk": "Активные отгрузки",
        "active_fleet": "Активный флот",
        "system_status": "Статус системы",
        "compliance": "Соответствие",
        "table_header": "Текущая база данных отгрузок и контейнеров",
        "col_sevk": "№ Отгрузки",
        "col_alici": "Получатель",
        "col_ulke": "Страна",
        "col_kap": "Места",
        "col_net": "Нетто (кг)",
        "col_durum": "Статус",
        "status_onayli": "Таможня одобрена",
        "status_seyirde": "В море",
        "status_teslim": "Доставка в порт",
        "status_gumrukte": "На таможне",
        "status_yol": "Отправлено",
        "status_yeni": "Новая запись",
        "map_gemi_title": "Радар морских судов и матрица местоположения",
        "map_gemi_desc": "Информация о местонахождении судов между международными портами в реальном времени.",
        "map_tir_title": "Матрица автопарка и маршрутов грузовиков",
        "map_tir_desc": "Карта местонахождения грузовиков на европейских автомагистралях.",
        "pdf_title": "Официальный таможенный PDF движок",
        "pdf_desc": "Создавайте официально опечатанные транспортные документы по таможенным правилам.",
        "gemi_matrix": "Матрица местоположения мирового морского флота",
        "tir_matrix": "Матрица местоположения международного автопарка",
        "btn_gemi": "Открыть живую карту судов MarineTraffic ↗",
        "btn_tir": "Открыть карту отслеживания грузовиков ↗",
        "form_sevk_no": "Номер отгрузки / декларации",
        "form_alici": "Официальное название компании-получателя",
        "form_ulke": "Страна назначения",
        "form_kap": "Количество упаковок",
        "form_net": "Вес нетто (кг)",
        "form_brut": "Вес брутто (кг)",
        "form_teslim": "Условия поставки Incoterms",
        "form_pdf_btn": "Создать и скачать официальный PDF-документ",
        "form_ekle_btn": "Добавить запись в базу данных",
        "success_pdf": "Операция успешна! Таможенный документ подготовлен.",
        "success_ekle": "успешно добавлено!",
        # Kalemler / Envanter Çevirileri
        "parca_banner_title": "➕ Добавить новую позицию инвентаря и деталь",
        "parca_banner_desc": "Зарегистрируйте код товара, название детали, тип материала, линию производства и начальный запас.",
        "parca_kod": "Код товара",
        "parca_ad": "Название детали",
        "parca_malzeme": "Тип материала",
        "parca_hat": "Производственная линия",
        "parca_stok": "Начальный запас",
        "parca_btn": "💾 Сохранить деталь в базу данных",
        "parca_success": "успешно добавлено в инвентарь!",
        "parca_table_header": "📋 База данных зарегистрированных позиций инвентаря",
        "col_p_kod": "Код товара",
        "col_p_ad": "Название детали",
        "col_p_malzeme": "Материал",
        "col_p_hat": "Линия",
        "col_p_stok": "Начальный запас",
        "site_1_title": "Министерство торговли",
        "site_1_desc": "Официальное законодательство и внешняя торговля.",
        "site_1_btn": "Перейти ↗",
        "site_2_title": "Электронное правительство Таможня",
        "site_2_desc": "Таможенные декларации.",
        "site_2_btn": "Перейти ↗",
        "site_3_title": "Министерство транспорта",
        "site_3_desc": "Портовые операции.",
        "site_3_btn": "Перейти ↗",
        "log_title": "Системные логи",
        "log_desc": "Отчет о состоянии фонового движка выполнения.",
        "unit_adet": "Шт",
        "unit_tasit": "Транспорт",
        "status_online": "Онлайн"
    },
    "العربية": {
        "title": "نظام تخطيط موارد الجمارك والخدمات اللوجستية",
        "subtitle": "مركز الشحن والعمليات المؤسسي المتكامل وفقاً للمادة 114 من اللائحة الجمركية.",
        "menu_dashboard": "لوحة التحكم الرئيسية",
        "menu_gemi": "خريطة السفن البحرية",
        "menu_tir": "خريطة أسطول الشاحنات",
        "menu_pdf": "مستند الشحن ومحرك PDF",
        "menu_ekle": "إضافة شحنة جديدة",
        "menu_parca_ekle": "إضافة بند مخزون جديد",
        "menu_siteler": "بوابات التجارة الرسمية",
        "menu_loglar": "سجلات النظام",
        "update_btn": "تحديث البيانات الحية والنظام",
        "total_sevk": "الشحنات النشطة",
        "active_fleet": "الأسطول النشط",
        "system_status": "حالة النظام",
        "compliance": "الامتثال",
        "table_header": "قاعدة بيانات الشحنات والحاويات الحالية",
        "col_sevk": "رقم الشحنة",
        "col_alici": "المستلم",
        "col_ulke": "الدولة",
        "col_kap": "الحزم",
        "col_net": "الوزن الصافي",
        "col_durum": "الحالة",
        "status_onayli": "معتمد جمركياً",
        "status_seyirde": "في البحر",
        "status_teslim": "تسليم الميناء",
        "status_gumrukte": "في الجمارك",
        "status_yol": "تم الإرسال",
        "status_yeni": "سجل جديد",
        "map_gemi_title": "رادار السفن البحرية ومصفوفة الموقع",
        "map_gemi_desc": "معلومات الموقع في الوقت الفعلي للسفن التي تبحر بين الموانئ الدولية.",
        "map_tir_title": "مصفوفة أسطول الشاحنات والمسارات",
        "map_tir_desc": "خريطة مواقع الشاحنات التي تنقل البضائع على الطرق السريعة الأوروبية.",
        "pdf_title": "محرك PDF الرسمي المعتمد جمركياً",
        "pdf_desc": "إنشاء مستندات شحن مختومة رسمياً تتوافق تماماً مع لوائح الجمارك.",
        "gemi_matrix": "مصفوفة موقع الأسطول البحري العالمي",
        "tir_matrix": "مصفوفة موقع أسطول الشاحنات الدولي",
        "btn_gemi": "فتح خريطة السفن الحية MarineTraffic ↗",
        "btn_tir": "فتح خريطة تتبع الشاحنات المباشرة ↗",
        "form_sevk_no": "رقم الشحنة / الإقرار",
        "form_alici": "الاسم الرسمي لشركة المستلم",
        "form_ulke": "الدولة المستهدفة",
        "form_kap": "عدد الحزم",
        "form_net": "الوزن الصافي (كغ)",
        "form_brut": "الوزن الإجمالي (كغ)",
        "form_teslim": "شروط التسليم Incoterms",
        "form_pdf_btn": "إنشاء وتحميل مستند PDF الرسمي",
        "form_ekle_btn": "إضافة السجل إلى قاعدة البيانات",
        "success_pdf": "تم بنجاح! تم إعداد مستند الشحن الجمركي.",
        "success_ekle": "تمت الإضافة بنجاح!",
        # Kalemler / Envanter Çevirileri
        "parca_banner_title": "➕ إضافة بند مخزون جديد وقسائم الأجزاء",
        "parca_banner_desc": "سجل رمز المنتج، اسم الجزء، نوع Material، خط الإنتاج المرتبط، وكمية المخزون الأولية.",
        "parca_kod": "رمز المنتج",
        "parca_ad": "اسم الجزء",
        "parca_malzeme": "نوع المادة (Material)",
        "parca_hat": "خط الإنتاج المرتبط",
        "parca_stok": "كمية المخزون الأولية",
        "parca_btn": "💾 حفظ الجزء في قاعدة البيانات",
        "parca_success": "تمت الإضافة بنجاح إلى المخزون!",
        "parca_table_header": "📋 قاعدة بيانات بنود المخزون المسجلة",
        "col_p_kod": "رمز المنتج",
        "col_p_ad": "اسم الجزء",
        "col_p_malzeme": "المادة",
        "col_p_hat": "خط الإنتاج",
        "col_p_stok": "المخزون الأولي",
        "site_1_title": "وزارة التجارة",
        "site_1_desc": "التشريعات الرسمية والتجارة الخارجية.",
        "site_1_btn": "زيارة الموقع ↗",
        "site_2_title": "الجمارك الحكومية الإلكترونية",
        "site_2_desc": "إجراءات الإقرار الجمركي.",
        "site_2_btn": "زيارة الموقع ↗",
        "site_3_title": "وزارة النقل",
        "site_3_desc": "عمليات الموانئ.",
        "site_3_btn": "زيارة الموقع ↗",
        "log_title": "سجلات النظام",
        "log_desc": "تقرير حالة محرك التنفيذ في الخلفية.",
        "unit_adet": "وحدة",
        "unit_tasit": "مركبة",
        "status_online": "متصل"
    }
}

# --- CSS: MOR VE GRİ TONLARI ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(15, 15, 25, 0.78), rgba(26, 26, 46, 0.88)), 
                    url('https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    h1, h2, h3, h4 { 
        color: #f8fafc !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    p, span, label { 
        color: #e2e8f0 !important; 
    }
    .stButton>button {
        width: 100%;
        background: #4a5568;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 10px;
        border: 1px solid #718096;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover { 
        background: #718096;
        border-color: #a0aec0;
    }
    .clean-banner {
        background: rgba(45, 55, 72, 0.85);
        padding: 25px;
        border-radius: 8px;
        border-left: 5px solid #9f7aea;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-right: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    .clean-panel {
        background: rgba(45, 55, 72, 0.85);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DİL SEÇİMİ (SOL MENÜ) ---
with st.sidebar:
    st.markdown("### 🌐 **Dil / Language**")
    selected_lang = st.selectbox("Select Language", list(TRANSLATIONS.keys()), index=0)
    st.divider()

t = TRANSLATIONS[selected_lang]

# --- VERİTABANLARI ---
if "sevk_veritabani" not in st.session_state:
    st.session_state.sevk_veritabani = [
        {"Sevk No": "SEVK-2026-001", "Alıcı": "Ornek Dis Ticaret A.S.", "Ülke": "Almanya", "Kap": 50, "Net (Kg)": 1200, "Durum": t["status_onayli"]},
        {"Sevk No": "SEVK-2026-002", "Alıcı": "Mugla Global Lojistik", "Ülke": "İngiltere", "Kap": 120, "Net (Kg)": 3400, "Durum": t["status_onayli"]},
        {"Sevk No": "SEVK-2026-003", "Alıcı": "Akdeniz Ithalat Ltd.", "Ülke": "Fransa", "Kap": 30, "Net (Kg)": 850, "Durum": t["status_gumrukte"]}
    ]

if "parca_veritabani" not in st.session_state:
    st.session_state.parca_veritabani = [
        {"Ürün Kodu": "PRC-101", "Parça Adı": "CNC Torna Kesici Uç", "Malzeme": "Karbit Çelik", "İlgili Üretim Hattı": "Hat-A (Freze)", "Başlangıç Stok": 2400},
        {"Ürün Kodu": "PRC-102", "Parça Adı": "Servo Motor Sürücüsü", "Malzeme": "Elektronik Devre", "İlgili Üretim Hattı": "Hat-B (Montaj)", "Başlangıç Stok": 310}
    ]

# --- SOL MENÜ ---
with st.sidebar:
    st.markdown("### ⚓ **T.C. GÜMRÜK & LOJİSTİK ERP**")
    st.markdown("<p style='color: #9f7aea; font-size: 13px; font-weight: bold;'>Global Operasyon Merkezi</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio(
        "Menu",
        [
            t["menu_dashboard"], 
            t["menu_gemi"], 
            t["menu_tir"], 
            t["menu_pdf"], 
            t["menu_ekle"], 
            t["menu_parca_ekle"],
            t["menu_siteler"], 
            t["menu_loglar"]
        ]
    )
    st.divider()
    st.caption("Antalya / Seydikemer Bölge Müdürlüğü")

# --- 1. ANA KONTROL PANELİ ---
if menu == t["menu_dashboard"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">⚓ {t['title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_guncelle, _ = st.columns([1, 4])
    with col_guncelle:
        if st.button(t["update_btn"]):
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h4>{t["total_sevk"]}</h4><h2 style="color:#d6bcfa;">{len(st.session_state.sevk_veritabani)} {t["unit_adet"]}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h4>{t["active_fleet"]}</h4><h2 style="color:#9f7aea;">48,520 {t["unit_tasit"]}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h4>{t["system_status"]}</h4><h2 style="color:#4ade80;">{t["status_online"]} 🟢</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h4>{t["compliance"]}</h4><h2 style="color:#facc15;">%100 (Md. 114)</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 📋 **{t['table_header']}**")
    
    df = pd.DataFrame(st.session_state.sevk_veritabani)
    df.columns = [t["col_sevk"], t["col_alici"], t["col_ulke"], t["col_kap"], t["col_net"], t["col_durum"]]
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- 2. DENİZ YOLU GEMİ HARİTASI ---
elif menu == t["menu_gemi"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">⚓ {t['map_gemi_title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['map_gemi_desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="clean-panel">
            <h3>🚢 {t['gemi_matrix']}</h3>
            <p><b>1. TCG Akdeniz-1:</b> Akdeniz Açıkları (36.88° K, 30.70° D) - Hız: 14.2 Knot</p>
            <p><b>2. Toros Lojistik-4:</b> Mersin Körfezi (36.81° K, 34.64° D) - Hız: 12.8 Knot</p>
            <br>
            <a href="https://www.marinetraffic.com" target="_blank">
                <button style="background:#4a5568; color:white; border:1px solid #718096; padding:12px 25px; border-radius:6px; font-weight:bold; cursor:pointer;">
                    {t['btn_gemi']}
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- 3. KARA YOLU TIR FİLO HARİTASI ---
elif menu == t["menu_tir"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">🚛 {t['map_tir_title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['map_tir_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="clean-panel">
            <h3>🚚 {t['tir_matrix']}</h3>
            <p><b>1. Plaka 07 GMR 42:</b> Edirne Sınır Kapısı (41.71° K, 26.56° D)</p>
            <p><b>2. Plaka 48 SEY 99:</b> Denizli Geçiş Noktası (37.77° K, 29.08° D)</p>
            <br>
            <a href="https://www.marinetraffic.com" target="_blank">
                <button style="background:#4a5568; color:white; border:1px solid #718096; padding:12px 25px; border-radius:6px; font-weight:bold; cursor:pointer;">
                    {t['btn_tir']}
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- 4. SEVK EVRAKI & PDF MOTORU ---
elif menu == t["menu_pdf"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">📦 {t['pdf_title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['pdf_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("pdf_uretim_formu"):
        col_a, col_b = st.columns(2)
        with col_a:
            sevk_no = st.text_input(t["form_sevk_no"], value="SEVK-2026-042")
            alici_unvan = st.text_input(t["form_alici"], value="Antalya Dış Ticaret A.Ş.")
            gidecegi_ulke = st.selectbox(t["form_ulke"], ["Almanya", "İngiltere", "Fransa", "İtalya", "Hollanda"])
        with col_b:
            kap_adedi = st.number_input(t["form_kap"], min_value=1, value=75)
            net_kg = st.number_input(t["form_net"], min_value=0.0, value=2450.50)
            teslim_sekli = st.selectbox(t["form_teslim"], ["FOB", "EXW", "CIF", "CFR", "DDP"])

        st.markdown("<br>", unsafe_allow_html=True)
        islem_onayi = st.form_submit_button(t["form_pdf_btn"])

    def pdf_uret(veri):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        story = []
        styles = getSampleStyleSheet()
        
        b_style = ParagraphStyle('BSt', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#0f172a'), alignment=1, spaceAfter=5)
        a_style = ParagraphStyle('ASt', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#9f7aea'), alignment=1, spaceAfter=15)

        story.append(Paragraph("<b>T.C. GÜMRÜK VE DIŞ TİCARET BAKANLIĞI</b>", b_style))
        story.append(Paragraph("<b>SEVK EVRAKI VE NAKLİYE UYUM BELGESİ (Md. 114)</b>", a_style))
        story.append(Spacer(1, 10))
        
        tablo_verisi = [
            ["Sevk Numarası:", veri['sevk_no']],
            ["Alıcı Firma:", veri['alici']],
            ["Hedef Ülke:", veri['ulke']],
            ["Kap Adedi:", f"{veri['kap']} {t['unit_adet']}"],
            ["Net Ağırlık:", f"{veri['net_kg']} KG"],
            ["Teslim Şekli:", veri['teslim_sekli']],
            ["Elektronik Doğrulama:", f"TR-GMRK-2026-{datetime.datetime.now().strftime('%f')[:6]}"],
            ["Düzenleme Tarihi:", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]
        ]
        
        t_obj = Table(tablo_verisi, colWidths=[180, 340])
        t_obj.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#0f172a')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1'))
        ]))
        story.append(t_obj)
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>[ GÜMRÜK ELEKTRONİK MÜHÜR ALANI ]</b><br/><i>Bu belge Gümrük Yönetmeliği 114. madde hükümleri gereğince elektronik ortamda üretilmiştir.</i>", ParagraphStyle('FSt', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#475569'), alignment=1)))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    if islem_onayi:
        veri = {"sevk_no": sevk_no, "alici": alici_unvan, "ulke": gidecegi_ulke, "kap": kap_adedi, "net_kg": net_kg, "teslim_sekli": teslim_sekli}
        pdf = pdf_uret(veri)
        st.success(t["success_pdf"])
        st.download_button(label="📥 PDF", data=pdf, file_name=f"Gumruk_Sevk_{sevk_no}.pdf", mime="application/pdf")

# --- 5. YENİ SEVK EKLE ---
elif menu == t["menu_ekle"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">{t['menu_ekle']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">Sisteme yeni bir sevk beyannamesi ekleyin.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("yeni_sevk"):
        y_no = st.text_input(t["form_sevk_no"], value=f"SEVK-2026-00{len(st.session_state.sevk_veritabani)+1}")
        y_alici = st.text_input(t["form_alici"], value="Örn: Akdeniz Lojistik A.Ş.")
        y_ulke = st.selectbox(t["form_ulke"], ["Almanya", "İngiltere", "Fransa", "İtalya", "Hollanda"])
        y_kap = st.number_input(t["form_kap"], min_value=1, value=50)
        y_net = st.number_input(t["form_net"], min_value=0.0, value=1500.0)
        
        ekle = st.form_submit_button(t["form_ekle_btn"])

    if ekle:
        st.session_state.sevk_veritabani.append({"Sevk No": y_no, "Alıcı": y_alici, "Ülke": y_ulke, "Kap": y_kap, "Net (Kg)": y_net, "Durum": t["status_yeni"]})
        st.success(f"✅ {y_no} {t['success_ekle']}")

# --- 6. YENİ ENVANTER KALEMİ EKLE (DİNAMİK ÇEVİRİLİ) ---
elif menu == t["menu_parca_ekle"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">{t['parca_banner_title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['parca_banner_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("yeni_parca_formu"):
        f_kod = st.text_input(t["parca_kod"], value=f"PRC-10{len(st.session_state.parca_veritabani)+1}")
        f_ad = st.text_input(t["parca_ad"], value="Örn: Lazer Kesim Başlığı")
        f_malzeme = st.text_input(t["parca_malzeme"], value="Örn: Titanyum Alaşım")
        f_hat = st.selectbox(t["parca_hat"], ["Hat-A (Freze)", "Hat-B (Montaj)", "Hat-C (Test)", "Genel Gümrük Deposu"])
        f_stok = st.number_input(t["parca_stok"], min_value=1, value=500)
        
        parca_kaydet = st.form_submit_button(t["parca_btn"])

    if parca_kaydet:
        yeni_parca = {
            "Ürün Kodu": f_kod,
            "Parça Adı": f_ad,
            "Malzeme": f_malzeme,
            "İlgili Üretim Hattı": f_hat,
            "Başlangıç Stok": f_stok
        }
        st.session_state.parca_veritabani.append(yeni_parca)
        st.success(f"✅ {f_kod} {t['parca_success']}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(t["parca_table_header"])
    
    df_parca = pd.DataFrame(st.session_state.parca_veritabani)
    df_parca.columns = [t["col_p_kod"], t["col_p_ad"], t["col_p_malzeme"], t["col_p_hat"], t["col_p_stok"]]
    st.dataframe(df_parca, use_container_width=True, hide_index=True)

# --- 7. RESMİ GÜMRÜK SİTELERİ ---
elif menu == t["menu_siteler"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">{t['menu_siteler']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">Mevzuat ve resmi sorgulamalar için dış bağlantılar.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h3>{t["site_1_title"]}</h3><p>{t["site_1_desc"]}</p><a href="https://www.ticaret.gov.tr" target="_blank"><button style="background:#4a5568; color:white; border:1px solid #718096; padding:8px 15px; border-radius:6px; cursor:pointer;">{t["site_1_btn"]}</button></a></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h3>{t["site_2_title"]}</h3><p>{t["site_2_desc"]}</p><a href="https://www.turkiye.gov.tr" target="_blank"><button style="background:#4a5568; color:white; border:1px solid #718096; padding:8px 15px; border-radius:6px; cursor:pointer;">{t["site_2_btn"]}</button></a></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="clean-panel" style="text-align:center;"><h3>{t["site_3_title"]}</h3><p>{t["site_3_desc"]}</p><a href="https://denizcilik.uab.gov.tr" target="_blank"><button style="background:#4a5568; color:white; border:1px solid #718096; padding:8px 15px; border-radius:6px; cursor:pointer;">{t["site_3_btn"]}</button></a></div>', unsafe_allow_html=True)

# --- 8. SİSTEM LOGLARI ---
elif menu == t["menu_loglar"]:
    st.markdown(f"""
        <div class="clean-banner">
            <h1 style="margin:0; color:#f8fafc; font-size:26px;">{t['log_title']}</h1>
            <p style="margin:8px 0 0 0; color:#cbd5e1; font-size:14px;">{t['log_desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("Sistem Çekirdeği: Python & Streamlit Lojistik Motoru Aktif.")
    st.subheader("Son Sistem Logları")
    st.code("""
    [2026-10-12 03:10:00] INFO: T.C. Gümrük ve Lojistik ERP başlatıldı.
    [2026-10-12 03:12:30] TRANSLATION: Tam dinamik tablo, form ve envanter çeviri motoru aktif.
    [2026-10-12 03:15:12] DATABASE: Sevk ve parça envanter veritabanı senkronize edildi.
    [2026-10-12 03:18:45] SECURITY: Gümrük Md. 114 denetim filtresi aktif.
    """, language="text")
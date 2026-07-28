import os
import subprocess
import threading
import time
import locale
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk, filedialog

# 14 Popüler Dil Sözlüğü
LANGUAGES = {
    "Türkçe": {
        "title": "Evrensel Linux Canlı ISO Oluşturucu", "info": "Bu uygulama sisteminizi birebir içeren açılabilir bir ISO üretecektir.",
        "status_wait": "Durum: Bekliyor...", "btn_start": "Sistemi ISO olarak Klonla", "pwd_title": "Parola Gerekli",
        "pwd_msg": "İşlemleri başlatmak için root (sudo) şifrenizi giriniz:", "cancel_title": "İptal Edildi", "cancel_msg": "Şifre girilmedi.",
        "btn_progress": "İşlem Sürüyor...", "log_check": "[SİSTEM] Kontroller başlatılıyor...\n", "log_detected": "[SİSTEM] Tespit edilen Linux tabanı: ",
        "log_pkg": "[SİSTEM] Gerekli paketler ve bağımlılıklar kuruluyor...\n", "log_eggs_missing": "[SİSTEM] 'eggs' aracı bulunamadı. Derleme başlatılıyor...\n",
        "log_eggs_ok": "[SİSTEM] 'eggs' başarıyla kuruldu! Klonlama başlıyor...\n", "log_parrot": "[SİSTEM] Parrot OS algılandı, uyumluluk modu aktif...\n",
        "log_building": "[SİSTEM] Canlı ISO imajı inşa ediliyor (Bu işlem uzun sürebilir)...\n", "log_moving": "[SİSTEM] ISO dosyası seçtiğiniz konuma taşınıyor...\n",
        "log_success": "[BAŞARILI] İşlem tamamlandı! ISO dosyanız hazır.\n", "msg_success": "Sistem başarıyla klonlandı! ISO dosyası şu konumda:",
        "btn_show_term": "Terminali Göster", "btn_hide_term": "Terminali Gizle",
        "save_dialog_title": "ISO Dosyasını Kaydet", "time_elapsed": "Geçen süre:", "time_remaining": "Tahmini kalan süre:", "time_calculating": "Hesaplanıyor...",
        "btn_copy_log": "Logu Kopyala", "log_copied_msg": "Terminal içeriği panoya kopyalandı."
    },
    "English": {
        "title": "Universal Linux Live ISO Creator", "info": "This app will produce a bootable ISO containing an exact clone of your system.",
        "status_wait": "Status: Waiting...", "btn_start": "Clone System to ISO", "pwd_title": "Password Required",
        "pwd_msg": "Enter your root (sudo) password to start processes:", "cancel_title": "Canceled", "cancel_msg": "Password not entered.",
        "btn_progress": "Processing...", "log_check": "[SYSTEM] Controls starting...\n", "log_detected": "[SYSTEM] Detected Linux base: ",
        "log_pkg": "[SYSTEM] Installing required packages and dependencies...\n", "log_eggs_missing": "[SYSTEM] 'eggs' tool not found. Starting compilation...\n",
        "log_eggs_ok": "[SYSTEM] 'eggs' installed successfully! Cloning starting...\n", "log_parrot": "[SYSTEM] Parrot OS detected, compatibility mode active...\n",
        "log_building": "[SYSTEM] Building Live ISO image (This might take a while)...\n", "log_moving": "[SYSTEM] Moving ISO file to chosen location...\n",
        "log_success": "[SUCCESS] Process completed! Your ISO file is ready.\n", "msg_success": "System cloned successfully! ISO file is at:",
        "btn_show_term": "Show Terminal", "btn_hide_term": "Hide Terminal",
        "save_dialog_title": "Save ISO File", "time_elapsed": "Elapsed:", "time_remaining": "Estimated remaining:", "time_calculating": "Calculating...",
        "btn_copy_log": "Copy Log", "log_copied_msg": "Terminal content copied to clipboard."
    },
    "Español": {
        "title": "Creador Universal de ISO en Vivo de Linux", "info": "Esta aplicación producirá una ISO de arranque que contiene un clon exacto.",
        "status_wait": "Estado: Esperando...", "btn_start": "Clonar Sistema a ISO", "pwd_title": "Contraseña Requerida",
        "pwd_msg": "Ingrese su contraseña de root (sudo) para comenzar:", "cancel_title": "Cancelado", "cancel_msg": "Contraseña no ingresada.",
        "btn_progress": "Procesando...", "log_check": "[SISTEMA] Iniciando controles...\n", "log_detected": "[SISTEMA] Base Linux detectada: ",
        "log_pkg": "[SISTEMA] Instalando paquetes y dependencias necesarios...\n", "log_eggs_missing": "[SISTEMA] No se encontró la herramienta 'eggs'. Iniciando compilación...\n",
        "log_eggs_ok": "[SISTEMA] ¡'eggs' instalado con éxito! Iniciando clonación...\n", "log_parrot": "[SISTEMA] Parrot OS detectado, modo de compatibilidad activo...\n",
        "log_building": "[SISTEMA] Creando imagen ISO en vivo (Esto puede tardar)...\n", "log_moving": "[SISTEMA] Moviendo el archivo ISO a la ubicación elegida...\n",
        "log_success": "[ÉXITO] ¡Proceso completado! Su archivo ISO está listo.\n", "msg_success": "¡Sistema clonado con éxito! El archivo ISO está en:",
        "btn_show_term": "Mostrar Terminal", "btn_hide_term": "Ocultar Terminal",
        "save_dialog_title": "Guardar archivo ISO", "time_elapsed": "Transcurrido:", "time_remaining": "Restante estimado:", "time_calculating": "Calculando...",
        "btn_copy_log": "Copiar registro", "log_copied_msg": "Contenido de la terminal copiado al portapapeles."
    },
    "Français": {
        "title": "Créateur d'ISO Live Linux Universel", "info": "Cette application produira un ISO amorçable contenant un clone exact.",
        "status_wait": "Statut: En attente...", "btn_start": "Cloner le système en ISO", "pwd_title": "Mot de passe requis",
        "pwd_msg": "Entrez votre mot de passe root (sudo) :", "cancel_title": "Annulé", "cancel_msg": "Mot de passe non saisi.",
        "btn_progress": "Traitement...", "log_check": "[SYSTÈME] Démarrage des contrôles...\n", "log_detected": "[SYSTÈME] Base Linux détectée: ",
        "log_pkg": "[SYSTÈME] Installation des paquets requis...\n", "log_eggs_missing": "[SYSTÈME] Outil 'eggs' non trouvé. Début de la compilation...\n",
        "log_eggs_ok": "[SYSTÈME] 'eggs' installé avec succès! Début du clonage...\n", "log_parrot": "[SYSTÈME] Parrot OS détecté, mode de compatibilité actif...\n",
        "log_building": "[SYSTÈME] Génération de l'image ISO (Cela peut prendre du temps)...\n", "log_moving": "[SYSTÈME] Déplacement du fichier ISO vers l'emplacement choisi...\n",
        "log_success": "[SUCCÈS] Processus terminé! Votre fichier ISO est prêt.\n", "msg_success": "Système cloné avec succès! Le fichier ISO se trouve à:",
        "btn_show_term": "Afficher le terminal", "btn_hide_term": "Masquer le terminal",
        "save_dialog_title": "Enregistrer le fichier ISO", "time_elapsed": "Écoulé:", "time_remaining": "Restant estimé:", "time_calculating": "Calcul en cours...",
        "btn_copy_log": "Copier le journal", "log_copied_msg": "Contenu du terminal copié dans le presse-papiers."
    },
    "Deutsch": {
        "title": "Universeller Linux Live ISO Ersteller", "info": "Diese App erstellt eine bootfähige ISO, die einen exakten Klon enthält.",
        "status_wait": "Status: Warten...", "btn_start": "System als ISO klonen", "pwd_title": "Passwort erforderlich",
        "pwd_msg": "Geben Sie Ihr Root-Passwort (sudo) ein:", "cancel_title": "Abgebrochen", "cancel_msg": "Passwort nicht eingegeben.",
        "btn_progress": "In Bearbeitung...", "log_check": "[SYSTEM] Kontrollen werden gestartet...\n", "log_detected": "[SYSTEM] Erkannte Linux-Basis: ",
        "log_pkg": "[SYSTEM] Notwendige Pakete werden installiert...\n", "log_eggs_missing": "[SYSTEM] Werkzeug 'eggs' nicht gefunden. Kompilierung startet...\n",
        "log_eggs_ok": "[SYSTEM] 'eggs' erfolgreich installiert! Klonen startet...\n", "log_parrot": "[SYSTEM] Parrot OS erkannt, Kompatibilitätsmodus aktiv...\n",
        "log_building": "[SYSTEM] Live-ISO-Image wird erstellt (Dies kann dauern)...\n", "log_moving": "[SYSTEM] ISO-Datei wird an den gewählten Ort verschoben...\n",
        "log_success": "[ERFOLG] Prozess abgeschlossen! Ihre ISO-Datei ist bereit.\n", "msg_success": "System erfolgreich geklont! Die ISO-Datei befindet sich unter:",
        "btn_show_term": "Terminal anzeigen", "btn_hide_term": "Terminal ausblenden",
        "save_dialog_title": "ISO-Datei speichern", "time_elapsed": "Verstrichen:", "time_remaining": "Geschätzte Restzeit:", "time_calculating": "Berechne...",
        "btn_copy_log": "Protokoll kopieren", "log_copied_msg": "Terminalinhalt in die Zwischenablage kopiert."
    },
    "Italiano": {
        "title": "Creatore ISO Live Linux Universale", "info": "Questa applicazione produrrà un ISO avviabile contenente un clone esatto.",
        "status_wait": "Stato: In attesa...", "btn_start": "Clona Sistema in ISO", "pwd_title": "Password Richiesta",
        "pwd_msg": "Inserisci la password di root (sudo):", "cancel_title": "Annullato", "cancel_msg": "Password non inserita.",
        "btn_progress": "In corso...", "log_check": "[SISTEMA] Avvio controlli...\n", "log_detected": "[SISTEMA] Base Linux rilevata: ",
        "log_pkg": "[SISTEMA] Installazione pacchetti richiesti...\n", "log_eggs_missing": "[SISTEMA] Strumento 'eggs' non trovato. Avvio compilazione...\n",
        "log_eggs_ok": "[SISTEMA] 'eggs' installato con successo! Avvio clonazione...\n", "log_parrot": "[SISTEMA] Parrot OS rilevato, modalità compatibilità attiva...\n",
        "log_building": "[SISTEMA] Creazione dell'immagine ISO Live (Può richiedere tempo)...\n", "log_moving": "[SISTEMA] Spostamento del file ISO nella posizione scelta...\n",
        "log_success": "[SUCCESSO] Processo completato! Il file ISO è pronto.\n", "msg_success": "Sistema clonato con successo! Il file ISO si trova in:",
        "btn_show_term": "Mostra Terminale", "btn_hide_term": "Nascondi Terminale",
        "save_dialog_title": "Salva file ISO", "time_elapsed": "Trascorso:", "time_remaining": "Rimanente stimato:", "time_calculating": "Calcolo in corso...",
        "btn_copy_log": "Copia registro", "log_copied_msg": "Contenuto del terminale copiato negli appunti."
    },
    "Português": {
        "title": "Criador Universal de ISO Live Linux", "info": "Este aplicativo produzirá um ISO inicializável contendo um clone exato.",
        "status_wait": "Status: Aguardando...", "btn_start": "Clonar Sistema para ISO", "pwd_title": "Senha Necessária",
        "pwd_msg": "Digite sua senha de root (sudo):", "cancel_title": "Cancelado", "cancel_msg": "Senha não informada.",
        "btn_progress": "Processando...", "log_check": "[SISTEMA] Iniciando verificações...\n", "log_detected": "[SISTEMA] Base Linux detectada: ",
        "log_pkg": "[SISTEMA] Instalando pacotes necessários...\n", "log_eggs_missing": "[SISTEMA] Ferramenta 'eggs' não encontrada. Iniciando compilação...\n",
        "log_eggs_ok": "[SISTEMA] 'eggs' instalado com sucesso! Iniciando clonagem...\n", "log_parrot": "[SISTEMA] Parrot OS detetado, modo de compatibilidade ativo...\n",
        "log_building": "[SISTEMA] Construindo imagem ISO Live (Isto pode demorar)...\n", "log_moving": "[SISTEMA] Movendo o arquivo ISO para o local escolhido...\n",
        "log_success": "[SUCESSO] Processo concluído! O arquivo ISO está pronto.\n", "msg_success": "Sistema clonado com sucesso! O arquivo ISO está em:",
        "btn_show_term": "Mostrar Terminal", "btn_hide_term": "Ocultar Terminal",
        "save_dialog_title": "Salvar arquivo ISO", "time_elapsed": "Decorrido:", "time_remaining": "Restante estimado:", "time_calculating": "Calculando...",
        "btn_copy_log": "Copiar registro", "log_copied_msg": "Conteúdo do terminal copiado para a área de transferência."
    },
    "Русский": {
        "title": "Универсальный создатель Live ISO для Linux", "info": "Это приложение создаст загрузочный ISO, содержащий точную копию.",
        "status_wait": "Статус: Ожидание...", "btn_start": "Клонировать систему в ISO", "pwd_title": "Требуется пароль",
        "pwd_msg": "Введите пароль root (sudo):", "cancel_title": "Отменено", "cancel_msg": "Пароль не введен.",
        "btn_progress": "В процессе...", "log_check": "[СИСТЕМА] Запуск проверок...\n", "log_detected": "[СИСТЕМА] Обнаружена база Linux: ",
        "log_pkg": "[СИСТЕМА] Установка необходимых пакетов...\n", "log_eggs_missing": "[СИСТЕМА] Инструмент 'eggs' не найден. Начало компиляции...\n",
        "log_eggs_ok": "[СИСТЕМА] 'eggs' успешно установлен! Начало клонирования...\n", "log_parrot": "[СИСТЕМА] Обнаружена Parrot OS, активен режим совместимости...\n",
        "log_building": "[СИСТЕМА] Сборка Live ISO образа (Это может занять время)...\n", "log_moving": "[СИСТЕМА] Перемещение ISO файла в выбранное место...\n",
        "log_success": "[УСПЕХ] Процесс завершен! Ваш ISO файл готов.\n", "msg_success": "Система успешно клонирована! ISO файл находится по пути:",
        "btn_show_term": "Показать терминал", "btn_hide_term": "Скрыть терминал",
        "save_dialog_title": "Сохранить файл ISO", "time_elapsed": "Прошло:", "time_remaining": "Осталось (примерно):", "time_calculating": "Вычисление...",
        "btn_copy_log": "Скопировать журнал", "log_copied_msg": "Содержимое терминала скопировано в буфер обмена."
    },
    "中文": {
        "title": "通用 Linux Live ISO 生成器", "info": "此应用程序将生成一个包含系统精确克隆的启动 ISO。",
        "status_wait": "状态: 等待中...", "btn_start": "将系统克隆为 ISO", "pwd_title": "需要密码",
        "pwd_msg": "请输入您的 root (sudo) 密码:", "cancel_title": "已取消", "cancel_msg": "未输入密码。",
        "btn_progress": "处理中...", "log_check": "[系统] 开始检查...\n", "log_detected": "[系统] 检测到的 Linux 发行版基底: ",
        "log_pkg": "[系统] 正在安装所需的包和依赖项...\n", "log_eggs_missing": "[系统] 未找到 'eggs' 工具。开始编译...\n",
        "log_eggs_ok": "[系统] 'eggs' 安装成功！开始克隆...\n", "log_parrot": "[系统] 检测到 Parrot OS，兼容模式已激活...\n",
        "log_building": "[系统] 正在构建 Live ISO 镜像 (这可能需要一些时间)...\n", "log_moving": "[系统] 正在将 ISO 文件移动到所选位置...\n",
        "log_success": "[成功] 流程完成！您的 ISO 文件已准备就绪。\n", "msg_success": "系统克隆成功！ISO 文件位于:",
        "btn_show_term": "显示终端", "btn_hide_term": "隐藏终端",
        "save_dialog_title": "保存 ISO 文件", "time_elapsed": "已用时间:", "time_remaining": "预计剩余:", "time_calculating": "计算中...",
        "btn_copy_log": "复制日志", "log_copied_msg": "终端内容已复制到剪贴板。"
    },
    "日本語": {
        "title": "万能 Linux Live ISO クリエイター", "info": "このアプリは、システムの完全なクローンを含む起動可能なISOを作成します。",
        "status_wait": "ステータス: 待機中...", "btn_start": "システムをISOにクローン", "pwd_title": "パスワードが必要",
        "pwd_msg": "root (sudo) パスワードを入力してください:", "cancel_title": "キャンセル", "cancel_msg": "パスワードが入力されていません。",
        "btn_progress": "処理中...", "log_check": "[システム] チェックを開始しています...\n", "log_detected": "[システム] 検出されたLinuxベース: ",
        "log_pkg": "[システム] 必要なパッケージと依存関係をインストール中...\n", "log_eggs_missing": "[システム] 'eggs'ツールが見つかりません。コンパイルを開始します...\n",
        "log_eggs_ok": "[システム] 'eggs' のインストールに成功しました！クローンを開始します...\n", "log_parrot": "[システム] Parrot OSを検出、互換モードが有効です...\n",
        "log_building": "[システム] Live ISOイメージを構築中 (時間がかかる場合があります)...\n", "log_moving": "[システム] ISOファイルを選択した場所に移動中...\n",
        "log_success": "[成功] プロセス完了！ISOファイルの準備ができました。\n", "msg_success": "システムのクローンに成功しました！ISOファイルの場所:",
        "btn_show_term": "ターミナルを表示", "btn_hide_term": "ターミナルを非表示",
        "save_dialog_title": "ISOファイルを保存", "time_elapsed": "経過時間:", "time_remaining": "推定残り時間:", "time_calculating": "計算中...",
        "btn_copy_log": "ログをコピー", "log_copied_msg": "ターミナルの内容をクリップボードにコピーしました。"
    },
    "العربية": {
        "title": "منشئ أقراص Linux Live ISO العالمي", "info": "سيعمل هذا التطبيق على إنتاج نسخة ISO قابلة للإقلاع تحتوي على نسخة مطابقة لنظامك.",
        "status_wait": "الحالة: في الانتظار...", "btn_start": "استنساخ النظام إلى ISO", "pwd_title": "كلمة المرور مطلوبة",
        "pwd_msg": "أدخل كلمة مرور الـ root (sudo) لبدء العمليات:", "cancel_title": "تم الإلغاء", "cancel_msg": "لم يتم إدخال كلمة المرور.",
        "btn_progress": "جاري المعالجة...", "log_check": "[النظام] بدء الفحوصات...\n", "log_detected": "[النظام] قاعدة Linux المكتشفة: ",
        "log_pkg": "[النظام] جاري تثبيت الحزم المطلوبة والاعتماديات...\n", "log_eggs_missing": "[النظام] أداة 'eggs' غير موجودة. بدء التجميع...\n",
        "log_eggs_ok": "[النظام] تم تثبيت 'eggs' بنجاح! بدء الاستنساخ...\n", "log_parrot": "[النظام] تم اكتشاف Parrot OS، وضع التوافق نشط...\n",
        "log_building": "[النظام] جاري بناء صورة Live ISO (قد يستغرق هذا بعض الوقت)...\n", "log_moving": "[النظام] جاري نقل ملف ISO إلى الموقع المختار...\n",
        "log_success": "[نجاح] اكتملت العملية! ملف ISO جاهز.\n", "msg_success": "تم استنساخ النظام بنجاح! ملف ISO موجود في:",
        "btn_show_term": "إظهار الطرفية", "btn_hide_term": "إخفاء الطرفية",
        "save_dialog_title": "حفظ ملف ISO", "time_elapsed": "الوقت المنقضي:", "time_remaining": "الوقت المتبقي المقدر:", "time_calculating": "جارٍ الحساب...",
        "btn_copy_log": "نسخ السجل", "log_copied_msg": "تم نسخ محتوى الطرفية إلى الحافظة."
    },
    "हिन्दी": {
        "title": "यूनिवर्सल लिनक्स लाइव ISO क्रिएटर", "info": "यह ऐप आपके सिस्टम का सटीक क्लोन रखने वाला बूट करने योग्य ISO तैयार करेगा।",
        "status_wait": "स्थिति: प्रतीक्षा कर रहा है...", "btn_start": "सिस्टम को ISO में क्लोन करें", "pwd_title": "पासवर्ड आवश्यक",
        "pwd_msg": "प्रक्रियाओं को शुरू करने के लिए रूट (sudo) पासवर्ड दर्ज करें:", "cancel_title": "रद्द किया गया", "cancel_msg": "पासवर्ड दर्ज नहीं किया गया।",
        "btn_progress": "प्रक्रिया जारी है...", "log_check": "[सिस्टम] नियंत्रण शुरू हो रहा है...\n", "log_detected": "[सिस्टम] पाया गया लिनक्स बेस: ",
        "log_pkg": "[सिस्टम] आवश्यक पैकेज और निर्भरताएँ स्थापित की जा रही हैं...\n", "log_eggs_missing": "[सिस्टम] 'eggs' टूल नहीं मिला। संकलन शुरू हो रहा है...\n",
        "log_eggs_ok": "[सिस्टम] 'eggs' सफलतापूर्वक स्थापित! क्लोनिंग शुरू हो रही है...\n", "log_parrot": "[सिस्टम] Parrot OS पाया गया, अनुकूलता मोड सक्रिय...\n",
        "log_building": "[सिस्टम] लाइव ISO इमेज बनाई जा रही है (इसमें कुछ समय लग सकता है)...\n", "log_moving": "[सिस्टम] ISO फ़ाइल को चयनित स्थान पर ले जाया जा रहा है...\n",
        "log_success": "[सफलता] प्रक्रिया पूरी हुई! आपकी ISO फ़ाइल तैयार है।\n", "msg_success": "सिस्टम सफलतापूर्वक क्लोन किया गया! ISO फ़ाइल यहाँ है:",
        "btn_show_term": "टर्मिनल दिखाएं", "btn_hide_term": "टर्मिनल छुपाएं",
        "save_dialog_title": "ISO फ़ाइल सहेजें", "time_elapsed": "बीता समय:", "time_remaining": "अनुमानित शेष समय:", "time_calculating": "गणना हो रही है...",
        "btn_copy_log": "लॉग कॉपी करें", "log_copied_msg": "टर्मिनल सामग्री क्लिपबोर्ड पर कॉपी की गई।"
    },
    "Persian": {
        "title": "سازنده جهانی لینوکس لایو ایزو", "info": "این برنامه یک فایل ایزو قابل بوت حاوی شبیه‌سازی دقیق سیستم شما ایجاد می‌کند.",
        "status_wait": "وضعیت: در انتظار...", "btn_start": "شبیه‌سازی سیستم به ایزو", "pwd_title": "رمز عبور لازم است",
        "pwd_msg": "رمز عبور ریشه (sudo) خود را وارد کنید:", "cancel_title": "لغو شد", "cancel_msg": "رمز عبور وارد نشد.",
        "btn_progress": "در حال پردازش...", "log_check": "[سیستم] شروع بررسی‌ها...\n", "log_detected": "[سیستم] پایه لینوکس شناسایی شده: ",
        "log_pkg": "[سیستم] در حال نصب بسته‌ها و وابستگی‌های لازم...\n", "log_eggs_missing": "[سیستم] ابزار 'eggs' یافت نشد. شروع کامپایل...\n",
        "log_eggs_ok": "[سیستم] 'eggs' با موفقیت نصب شد! شروع شبیه‌سازی...\n", "log_parrot": "[سیستم] توزیع Parrot OS شناسایی شد، حالت سازگاری فعال است...\n",
        "log_building": "[سیستم] در حال ساخت ایمیج لایو ایزو (این کار ممکن است طول بکشد)...\n", "log_moving": "[سیستم] در حال انتقال فایل ایزو به مسیر انتخاب‌شده...\n",
        "log_success": "[موفقیت] فرآیند کامل شد! فایل ایزو شما آماده است.\n", "msg_success": "سیستم با موفقیت شبیه‌سازی شد! فایل ایزو در مسیر زیر است:",
        "btn_show_term": "نمایش ترمینال", "btn_hide_term": "مخفی کردن ترمینال",
        "save_dialog_title": "ذخیره فایل ISO", "time_elapsed": "زمان سپری‌شده:", "time_remaining": "زمان تخمینی باقی‌مانده:", "time_calculating": "در حال محاسبه...",
        "btn_copy_log": "کپی گزارش", "log_copied_msg": "محتوای ترمینال در کلیپ‌بورد کپی شد."
    },
    "Ukrainian": {
        "title": "Універсальний творець Live ISO для Linux", "info": "Ця програма створить завантажувальний ISO, що містить точну копію системи.",
        "status_wait": "Статус: Очікування...", "btn_start": "Клонувати систему в ISO", "pwd_title": "Потрібен пароль",
        "pwd_msg": "Введіть пароль root (sudo):", "cancel_title": "Скасовано", "cancel_msg": "Пароль не введено.",
        "btn_progress": "Обробка...", "log_check": "[СИСТЕМА] Запуск перевірок...\n", "log_detected": "[СИСТЕМА] Виявлено базу Linux: ",
        "log_pkg": "[СИСТЕМА] Встановлення необхідних пакетів...\n", "log_eggs_missing": "[СИСТЕМА] Інструмент 'eggs' не знайдено. Початок компіляції...\n",
        "log_eggs_ok": "[СИСТЕМА] 'eggs' успішно встановлено! Початок клонування...\n", "log_parrot": "[СИСТЕМА] Виявлено Parrot OS, активний режим сумісності...\n",
        "log_building": "[СИСТЕМА] Збирання Live ISO образу (Це може зайняти час)...\n", "log_moving": "[СИСТЕМА] Переміщення ISO файлу до обраного місця...\n",
        "log_success": "[УСПІХ] Процес завершено! Ваш ISO файл готовий.\n", "msg_success": "Систему успішно клоновано! ISO файл знаходиться за шляхом:",
        "btn_show_term": "Показати термінал", "btn_hide_term": "Приховати термінал",
        "save_dialog_title": "Зберегти файл ISO", "time_elapsed": "Минуло:", "time_remaining": "Орієнтовний залишок:", "time_calculating": "Обчислення...",
        "btn_copy_log": "Скопіювати журнал", "log_copied_msg": "Вміст термінала скопійовано в буфер обміну."
    }
}

# Sistem dilini yakalayıp uygulama diliyle eşleştirmek için
LOCALE_MAP = {
    'tr': 'Türkçe', 'en': 'English', 'es': 'Español', 'fr': 'Français',
    'de': 'Deutsch', 'it': 'Italiano', 'pt': 'Português', 'ru': 'Русский',
    'zh': '中文', 'ja': '日本語', 'ko': '한국어', 'ar': 'العربية',
    'hi': 'हिन्दी', 'fa': 'Persian', 'uk': 'Ukrainian'
}


def detect_distro_family():
    """/etc/os-release içindeki ID ve ID_LIKE alanlarına bakarak dağıtım ailesini bulur.
    Kapsanan aileler: debian (Debian/Ubuntu/Devuan/Mint/vb.), arch (Arch/Manjaro/EndeavourOS/vb.),
    fedora (Fedora/RHEL/CentOS/AlmaLinux/Rocky/vb.), suse (openSUSE/SLES), alpine (Alpine)."""
    os_release = {}
    if os.path.exists("/etc/os-release"):
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        k, v = line.split("=", 1)
                        os_release[k] = v.strip().strip('"')
        except Exception:
            pass

    combined = f"{os_release.get('ID', '')} {os_release.get('ID_LIKE', '')}".lower()

    if "alpine" in combined:
        return "alpine"
    if "arch" in combined or "manjaro" in combined:
        return "arch"
    if "suse" in combined:
        return "suse"
    if any(x in combined for x in ("fedora", "rhel", "centos", "rocky", "almalinux", "mageia")):
        return "fedora"
    if any(x in combined for x in ("debian", "ubuntu", "devuan")):
        return "debian"

    # os-release yoksa veya eşleşmezse eski dosya bazlı kontrole düş
    if os.path.exists("/etc/arch-release"):
        return "arch"
    if os.path.exists("/etc/fedora-release"):
        return "fedora"
    if os.path.exists("/etc/alpine-release"):
        return "alpine"
    if os.path.exists("/etc/SuSE-release"):
        return "suse"
    return "debian"


def detect_system_language():
    """İşletim sisteminin dilini algılayıp desteklenen dillerden birine eşler, bulamazsa İngilizce döner."""
    try:
        lang_code = os.environ.get('LANG') or os.environ.get('LC_ALL') or os.environ.get('LC_MESSAGES')
        if not lang_code:
            lang_code = locale.getlocale()[0]
        if lang_code:
            prefix = lang_code.split('_')[0].split('.')[0].lower()
            return LOCALE_MAP.get(prefix, "English")
    except Exception:
        pass
    return "English"


current_lang = detect_system_language()
terminal_visible = False
process_start_time = None
process_running = False
iso_save_path = None


def change_language(event=None):
    global current_lang
    current_lang = lang_combo.get()
    lang = LANGUAGES[current_lang]
    lbl_title.config(text=lang["title"])
    lbl_info.config(text=lang["info"])
    lbl_status.config(text=lang["status_wait"])
    btn_start.config(text=lang["btn_start"])
    btn_toggle_term.config(text=lang["btn_hide_term"] if terminal_visible else lang["btn_show_term"])
    btn_copy_log.config(text=lang["btn_copy_log"])
    if not process_running:
        lbl_time.config(text="")


def copy_terminal_log():
    """Terminal ekranındaki tüm metni panoya kopyalar, böylece kolayca yapıştırılıp paylaşılabilir."""
    lang = LANGUAGES[current_lang]
    content = text_terminal.get('1.0', tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()  # panoya kopyalanan içeriğin kalıcı olmasını sağlar
    messagebox.showinfo(lang["cancel_title"], lang["log_copied_msg"])


def toggle_terminal():
    global terminal_visible
    lang = LANGUAGES[current_lang]
    if terminal_visible:
        text_terminal.pack_forget()
        root.geometry("680x320")
        btn_toggle_term.config(text=lang["btn_show_term"])
        terminal_visible = False
    else:
        text_terminal.pack(pady=5, padx=15, before=frame_progress)
        root.geometry("680x600")
        btn_toggle_term.config(text=lang["btn_hide_term"])
        terminal_visible = True


def format_td(seconds):
    return str(datetime.timedelta(seconds=int(max(seconds, 0))))


def update_time_labels(progress_val):
    lang = LANGUAGES[current_lang]
    if not process_running or process_start_time is None:
        return
    elapsed = time.time() - process_start_time
    if progress_val and progress_val > 2:
        remaining = (elapsed / progress_val) * (100 - progress_val)
        remaining_text = format_td(remaining)
    else:
        remaining_text = lang["time_calculating"]
    lbl_time.config(text=f"{lang['time_elapsed']} {format_td(elapsed)}   |   {lang['time_remaining']} {remaining_text}")


def tick_timer():
    if process_running:
        update_time_labels(progress_bar['value'])
        root.after(1000, tick_timer)


def update_progress(val, status_text=None):
    progress_bar['value'] = val
    lbl_percentage.config(text=f"%{int(val)}")
    if status_text:
        lbl_status.config(text=status_text)


def gui_log(line):
    root.after(0, lambda: (text_terminal.insert(tk.END, line), text_terminal.see(tk.END)))


def gui_progress(val, status_text=None):
    root.after(0, lambda: update_progress(val, status_text))


def run_backup():
    global process_start_time, process_running, iso_save_path
    lang = LANGUAGES[current_lang]

    # Kullanıcıdan ISO'nun kaydedileceği yer ve dosya adını iste
    save_path = filedialog.asksaveasfilename(
        title=lang["save_dialog_title"],
        defaultextension=".iso",
        initialfile="linux-live.iso",
        filetypes=[("ISO", "*.iso")]
    )
    if not save_path:
        return
    iso_save_path = save_path

    password = simpledialog.askstring(lang["pwd_title"], lang["pwd_msg"], show='*')
    if not password:
        messagebox.showwarning(lang["cancel_title"], lang["cancel_msg"])
        return

    btn_start.config(state=tk.DISABLED, text=lang["btn_progress"])
    text_terminal.delete('1.0', tk.END)
    text_terminal.insert(tk.END, lang["log_check"])
    update_progress(5, lang["log_check"].strip())

    process_start_time = time.time()
    process_running = True
    tick_timer()

    def process():
        global process_running
        try:
            # Dağıtım Ailesini Bul (Debian, Arch, Fedora/RHEL, openSUSE, Alpine)
            distro_base = detect_distro_family()
            gui_log(f"{lang['log_detected']}{distro_base.upper()}\n")
            gui_progress(10)

            # Bağımlılık Kurulumu (her aile için kendi paket yöneticisi)
            if distro_base == "debian":
                pkg_cmd = f"echo '{password}' | sudo -S apt update && echo '{password}' | sudo -S apt install -y git build-essential gcc make golang debootstrap xorriso squashfs-tools python3-tk"
            elif distro_base == "arch":
                pkg_cmd = f"echo '{password}' | sudo -S pacman -Sy --needed --noconfirm git base-devel gcc make go squashfs-tools xorriso tk"
            elif distro_base == "fedora":
                pkg_cmd = f"echo '{password}' | sudo -S dnf check-update ; echo '{password}' | sudo -S dnf install -y git make gcc golang squashfs-tools xorriso python3-tkinter"
            elif distro_base == "suse":
                pkg_cmd = f"echo '{password}' | sudo -S zypper --non-interactive refresh && echo '{password}' | sudo -S zypper --non-interactive install git make gcc go squashfs xorriso python3-tk"
            elif distro_base == "alpine":
                pkg_cmd = f"echo '{password}' | sudo -S apk update && echo '{password}' | sudo -S apk add git build-base go squashfs-tools xorriso python3-tkinter"
            else:
                pkg_cmd = f"echo '{password}' | sudo -S apt update && echo '{password}' | sudo -S apt install -y git build-essential gcc make golang debootstrap xorriso squashfs-tools python3-tk"

            gui_log(lang["log_pkg"])
            proc = subprocess.Popen(pkg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                gui_log(line)
            proc.wait()
            gui_progress(25)

            # eggs Aracı Kontrolü ve Kurulumu
            check_eggs = subprocess.run("command -v eggs", shell=True, capture_output=True, text=True)
            eggs_present = check_eggs.returncode == 0 and check_eggs.stdout.strip() != ""

            if not eggs_present:
                gui_log(lang["log_eggs_missing"])
                # Kaynaktan elle derlemek yerine, projenin resmi evrensel kurulum
                # betiğini (fresh-eggs) kullanıyoruz: dağıtımı kendisi algılar,
                # gereken Node.js sürümünü kurar ve sisteme uygun penguins-eggs
                # paketini (APT deposu / AUR / vb.) kendisi indirip kurar.
                cmd_install_eggs = f"""
cd /tmp && rm -rf fresh-eggs &&
git clone https://github.com/pieroproietti/fresh-eggs.git &&
cd fresh-eggs &&
chmod +x fresh-eggs.sh &&
echo '{password}' | sudo -S ./fresh-eggs.sh
"""
                proc = subprocess.Popen(cmd_install_eggs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    gui_log(line)
                proc.wait()

                # Kurulumun gerçekten işe yarayıp yaramadığını doğrula
                check_after = subprocess.run("command -v eggs", shell=True, capture_output=True, text=True)
                if proc.returncode != 0 or check_after.returncode != 0 or not check_after.stdout.strip():
                    raise RuntimeError(
                        "penguins-eggs kurulumu başarısız oldu. Yukarıdaki terminal çıktısında "
                        "hata olup olmadığını kontrol edin (örn. internet erişimi, desteklenmeyen "
                        "dağıtım sürümü veya eksik bağımlılık olabilir)."
                    )
                gui_log(lang["log_eggs_ok"])
            gui_progress(40)

            # Parrot OS Hilesi
            is_parrot = False
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    if "ID=parrot" in f.read():
                        is_parrot = True
            if is_parrot:
                gui_log(lang["log_parrot"])
                subprocess.run(f"echo '{password}' | sudo -S cp /etc/os-release /etc/os-release.bak && echo '{password}' | sudo -S sed -i 's/^ID=parrot/ID=debian/' /etc/os-release", shell=True)

            # Klonlama Başlangıcı
            gui_progress(45, lang["log_building"].strip())
            cmd_eggs = f"echo '{password}' | sudo -S eggs produce --clone"
            proc = subprocess.Popen(cmd_eggs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            current_p = 45
            for line in proc.stdout:
                gui_log(line)
                if "Checking available disk space" in line:
                    current_p = 50
                elif "Task Execution:" in line:
                    current_p = min(current_p + 2, 85)
                elif "Area secured" in line:
                    current_p = 90
                gui_progress(current_p)
            proc.wait()

            if is_parrot:
                subprocess.run(f"echo '{password}' | sudo -S mv /etc/os-release.bak /etc/os-release", shell=True)

            # ISO'yu kullanıcının seçtiği konuma taşı ve yetkilendir
            gui_progress(95, lang["log_moving"].strip())
            dest_dir = os.path.dirname(iso_save_path) or "."
            os.makedirs(dest_dir, exist_ok=True)
            user_name = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"

            # eggs, ISO'yu /home/eggs/ altına sabit ".iso" adıyla değil, dağıtım
            # adı + tarih içeren bir isimle üretir. Bu yüzden dosyayı isme göre
            # değil, en son değiştirilen .iso dosyasını arayarak buluyoruz.
            find_cmd = (
                f"echo '{password}' | sudo -S find /home/eggs -maxdepth 2 -name '*.iso' "
                f"-printf '%T@ %p\\n' 2>/dev/null | sort -rn | head -n1 | cut -d' ' -f2-"
            )
            find_result = subprocess.run(find_cmd, shell=True, capture_output=True, text=True)
            source_iso = find_result.stdout.strip()

            if not source_iso:
                raise RuntimeError(
                    "/home/eggs altında üretilmiş bir .iso dosyası bulunamadı. "
                    "Yukarıdaki terminal çıktısında 'eggs produce --clone' komutunun "
                    "gerçekten tamamlanıp tamamlanmadığını kontrol edin."
                )

            gui_log(f"[SİSTEM] Bulunan ISO: {source_iso}\n")

            # mv ve chown ayrı komutlar olarak çalıştırılıyor: taşımanın başarısı
            # sahiplik ayarına bağlı olmasın. Özellikle FAT32/exFAT/NTFS formatlı
            # USB bellekler Unix sahiplik (uid/gid) kavramını desteklemediği için
            # chown burada hata verebilir, ama bu dosyanın taşınmadığı anlamına gelmez.
            move_cmd = f"echo '{password}' | sudo -S mv '{source_iso}' '{iso_save_path}'"
            move_result = subprocess.run(move_cmd, shell=True, capture_output=True, text=True)
            if move_result.stdout:
                gui_log(move_result.stdout)
            if move_result.returncode != 0 or not os.path.exists(iso_save_path):
                error_detail = move_result.stderr.strip() or move_result.stdout.strip() or "bilinmeyen hata"
                raise RuntimeError(f"ISO dosyası hedef konuma taşınamadı: {error_detail}")

            chown_cmd = f"echo '{password}' | sudo -S chown {user_name}:{user_name} '{iso_save_path}'"
            chown_result = subprocess.run(chown_cmd, shell=True, capture_output=True, text=True)
            if chown_result.returncode != 0:
                gui_log(
                    "[UYARI] Dosya sahipliği ayarlanamadı (muhtemelen hedef USB/harici disk "
                    "FAT32, exFAT veya NTFS formatında ve Unix sahiplik kavramını desteklemiyor). "
                    "Bu, dosyanın taşınmadığı anlamına gelmez; ISO dosyanız hedef konumda kullanılabilir durumda.\n"
                )

            gui_progress(100, lang["log_success"].strip())
            gui_log(lang["log_success"])
            final_path = iso_save_path
            root.after(0, lambda: messagebox.showinfo(lang["cancel_title"], f"{lang['msg_success']}\n{final_path}"))
        except Exception as e:
            err = str(e)
            gui_log(f"\n[HATA] {err}\n")
            root.after(0, lambda: messagebox.showerror("Error", err))
        finally:
            process_running = False
            root.after(0, lambda: btn_start.config(state=tk.NORMAL, text=lang["btn_start"]))

    threading.Thread(target=process, daemon=True).start()


# GUI Tasarımı
root = tk.Tk()
root.title("Universal Linux ISO Remaster UI")
root.geometry("680x320")
root.configure(bg="#1e1e1e")

# Dil Seçim Paneli
frame_top = tk.Frame(root, bg="#1e1e1e")
frame_top.pack(fill=tk.X, padx=15, pady=5)

lbl_lang = tk.Label(frame_top, text="Language:", fg="white", bg="#1e1e1e", font=("Arial", 9))
lbl_lang.pack(side=tk.LEFT, padx=5)

lang_combo = ttk.Combobox(frame_top, values=list(LANGUAGES.keys()), state="readonly", width=12)
lang_combo.set(current_lang)
lang_combo.pack(side=tk.LEFT, padx=5)
lang_combo.bind("<<ComboboxSelected>>", change_language)

# Terminal Gizle/Göster Butonu
btn_toggle_term = tk.Button(frame_top, text=LANGUAGES[current_lang]["btn_show_term"], font=("Arial", 8, "bold"), bg="#444444", fg="white", padx=5, command=toggle_terminal)
btn_toggle_term.pack(side=tk.RIGHT, padx=5)

btn_copy_log = tk.Button(frame_top, text=LANGUAGES[current_lang]["btn_copy_log"], font=("Arial", 8, "bold"), bg="#444444", fg="white", padx=5, command=copy_terminal_log)
btn_copy_log.pack(side=tk.RIGHT, padx=5)

lbl_title = tk.Label(root, text=LANGUAGES[current_lang]["title"], font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#1e1e1e")
lbl_title.pack(pady=5)

lbl_info = tk.Label(root, text=LANGUAGES[current_lang]["info"], font=("Arial", 9), fg="#b3b3b3", bg="#1e1e1e")
lbl_info.pack(pady=2)

# Terminal Ekranı (Başlangıçta gizli)
text_terminal = scrolledtext.ScrolledText(root, width=82, height=18, bg="#000000", fg="#00ff00", font=("Courier", 9))

# İlerleme Çubuğu Bölümü
frame_progress = tk.Frame(root, bg="#1e1e1e")
frame_progress.pack(fill=tk.X, padx=20, pady=5)

progress_bar = ttk.Progressbar(frame_progress, orient="horizontal", mode="determinate", length=540)
progress_bar.pack(side=tk.LEFT, padx=5, pady=5)

lbl_percentage = tk.Label(frame_progress, text="%0", font=("Arial", 10, "bold"), fg="#00ff00", bg="#1e1e1e", width=5)
lbl_percentage.pack(side=tk.LEFT, padx=5)

lbl_status = tk.Label(root, text=LANGUAGES[current_lang]["status_wait"], font=("Arial", 9, "italic"), fg="#a6a6a6", bg="#1e1e1e")
lbl_status.pack(pady=2)

# Geçen süre / tahmini kalan süre etiketi
lbl_time = tk.Label(root, text="", font=("Arial", 9, "bold"), fg="#4FC3F7", bg="#1e1e1e")
lbl_time.pack(pady=2)

btn_start = tk.Button(root, text=LANGUAGES[current_lang]["btn_start"], font=("Arial", 11, "bold"), bg="#107C41", fg="white", padx=20, pady=6, command=run_backup)
btn_start.pack(pady=10)

root.mainloop()

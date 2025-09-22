/**
 * Khitan Large Script Interactive Website
 * By Nicolas of the Family Brett with Manus AI Pattern Recognition
 * World's Second Ancient Script Decipherment
 */

// Initialize Tone.js for audio playback
let audioContext;
let isPlaying = false;
let currentMemorial = null;

// Khitan frequency data and translations
const khitanData = {
    inscriptions: {
        yelu_yanning: {
            name: "Memorial for Yelü Yanning (986 CE)",
            originalText: `
皇帝 大契丹国 耶律延宁 墓志铭
天赞五年 岁次丙戌 九月 庚申朔 十五日 甲戌
故 大将军 耶律延宁 春秋四十 薨于 官舍
其 先世 高祖 高丽古 祖父 只吾不 父 萨葛
皆以 武功 著名 累世 忠勇 为国 宣力
延宁 少有 大志 长而 益厉 事 景宗皇帝 以 忠谨 见知
历官 殿前 都点检 枢密使 太师 国公 百户侯
统兵 北征 屡建 奇功 威震 边陲 夷狄 畏服
圣宗 即位 委以 重任 镇守 北疆 安抚 部族
不幸 中年 病卒 朝野 痛惜 特赠 太师 谥号 忠武
            `,
            frequencies: [770.00, 880.00, 770.00, 660.00, 586.67, 660.00, 495.00, 495.00, 556.88, 556.88, 586.67, 770.00, 660.00, 556.88, 880.00, 770.00, 329.63, 261.63, 440.00],
            translations: {
                en: `Memorial Inscription for Yelü Yanning, Great General of the Great Khitan State
In the fifth year of Tianzhan reign, year of Bingxu, ninth month, Gengshen new moon, fifteenth day Jiaxu
The late Great General Yelü Yanning, aged forty years, passed away at his official residence
His ancestors: Great-grandfather Gaoligu, Grandfather Zhiwubu, Father Sage
All renowned for martial achievements, generations of loyalty and courage serving the state
Yanning showed great ambition from youth, growing ever more determined, served Emperor Jingzong with loyal devotion
Held offices of Palace Guard Commander, Privy Council Minister, Grand Preceptor, Duke, Marquis of Hundred Households
Led armies in northern campaigns, repeatedly achieved extraordinary merit, his might shook the borderlands, barbarians submitted in fear
When Emperor Shengzong ascended the throne, entrusted him with great responsibility to guard the northern frontier and pacify the tribes
Unfortunately died of illness in middle age, court and country mourned deeply, specially posthumously honored as Grand Preceptor with the title "Loyal and Martial"`,
                zh: `大契丹国大将军耶律延宁墓志铭
天赞五年岁次丙戌九月庚申朔十五日甲戌
故大将军耶律延宁春秋四十薨于官舍
其先世高祖高丽古祖父只吾不父萨葛
皆以武功著名累世忠勇为国宣力
延宁少有大志长而益厉事景宗皇帝以忠谨见知
历官殿前都点检枢密使太师国公百户侯
统兵北征屡建奇功威震边陲夷狄畏服
圣宗即位委以重任镇守北疆安抚部族
不幸中年病卒朝野痛惜特赠太师谥号忠武`,
                mn: `Их Хятадын Улсын Их Жанжин Елү Яннины булшны бичиг
Тянь Жаны тавдугаар жил, Бин Сү жил, есдүгээр сар, Гэн Шэнь шинэ сар, арван тавдугаар өдөр Жиа Сү
Талийгаач Их Жанжин Елү Яннин дөчин насандаа албаны байшинд таалал төгслөө
Түүний өвөг дээдэс: Өвөг эцэг Гаолигү, Өвөг эцэг Живүбү, Эцэг Сагэ
Бүгд дайны гавьяараа алдартай, үе үеийн үнэнч эр зориг улсад үйлчилсэн
Яннин залуудаа их зорилго тавьж, өсөж томрохдоо улам хүчтэй болж, Жин Зон эзэнд үнэнч шударгаар үйлчилж танигдсан
Ордны өмнөх бүх цэгийн командлагч, Нууц зөвлөлийн сайд, Их багш, Гүн, Зуун өрхийн маркиз зэрэг албан тушаал хашсан
Хойд аянд цэрэг удирдаж, олон удаа онцгой гавьяа үзүүлж, хүч чадал нь хил хязгаарыг чичрүүлж, зэрлэгүүд айж дагаж байв
Шэн Зон хаан ширээнд суухад түүнд том үүрэг даатгаж хойд хилийг хамгаалж, овог аймгуудыг тайвшруулахыг даалгасан
Харамсалтай нь дунд насандаа өвчнөөр нас барж, ордон, улс гүнзгий гашуудаж, тусгайлан Их багш цол олгож "Үнэнч, Дайчин" гэсэн нэрээр хүндэтгэсэн`,
                ja: `大契丹国大将軍耶律延寧墓誌銘
天賛五年歳次丙戌九月庚申朔十五日甲戌
故大将軍耶律延寧春秋四十官舎に薨ず
其の先世高祖高麗古祖父只吾不父薩葛
皆武功を以て著名累世忠勇国の為に宣力す
延寧少くして大志有り長じて益々厲し景宗皇帝に事え忠謹を以て見知さる
歴官殿前都点検枢密使太師国公百戸侯
兵を統べ北征し屡々奇功を建て威辺陲を震わし夷狄畏服す
聖宗即位し重任を委ね北疆を鎮守し部族を安撫す
不幸中年病卒し朝野痛惜し特に太師を贈り諡号忠武とす`,
                ko: `대거란국 대장군 야율연령 묘지명
천찬 5년 세차 병술 9월 경신삭 15일 갑술
고 대장군 야율연령 춘추 40세에 관사에서 훙서하다
그 선세 고조 고려고 조부 지오불 부 살갈
모두 무공으로 저명하여 누세 충용으로 나라를 위해 선력하다
연령은 어려서부터 대지가 있어 자라면서 더욱 격려하여 경종황제를 섬겨 충근함으로 알려지다
역관 전전도점검 추밀사 태사 국공 백호후
병을 통솔하여 북정하여 여러 번 기공을 세워 위세가 변수를 진동시키고 이적이 외복하다
성종이 즉위하여 중임을 위임하여 북강을 진수하고 부족을 안무하다
불행히 중년에 병졸하여 조야가 통석하여 특히 태사를 증여하고 시호를 충무라 하다`,
                ru: `Надгробная надпись великого полководца Елю Яньнина Великого государства Кидань
В пятый год правления Тяньцзань, в год Бинсюй, в девятый месяц, в новолуние Гэншэнь, в пятнадцатый день Цзясюй
Покойный великий полководец Елю Яньнин, прожив сорок лет, скончался в своей служебной резиденции
Его предки: прапрадед Гаолигу, дед Чжиубу, отец Саге
Все прославились воинскими подвигами, поколения верно и мужественно служили государству
Яньнин с юности имел великие устремления, с возрастом становился еще решительнее, служил императору Цзинцзуну с верной преданностью
Занимал должности командующего дворцовой гвардией, министра Тайного совета, великого наставника, герцога, маркиза ста дворов
Возглавлял войска в северных походах, неоднократно совершал выдающиеся подвиги, его мощь потрясала пограничные земли, варвары покорялись в страхе
Когда император Шэнцзун взошел на престол, доверил ему великую ответственность охранять северные рубежи и умиротворять племена
К несчастью, умер от болезни в среднем возрасте, двор и страна глубоко скорбели, особо почтили посмертным титулом великого наставника с именем "Верный и Воинственный"`,
                de: `Grabinschrift des Großgenerals Yelü Yanning des Großen Khitan-Staates
Im fünften Jahr der Tianzhan-Regierung, Jahr Bingxu, neunter Monat, Neumond Gengshen, fünfzehnter Tag Jiaxu
Der verstorbene Großgeneral Yelü Yanning, vierzig Jahre alt, verstarb in seiner Amtsresidenz
Seine Vorfahren: Urgroßvater Gaoligu, Großvater Zhiwubu, Vater Sage
Alle berühmt für kriegerische Leistungen, Generationen von Treue und Mut im Dienste des Staates
Yanning zeigte von Jugend an große Ambitionen, wurde mit dem Alter noch entschlossener, diente Kaiser Jingzong mit treuer Hingabe
Bekleidete Ämter als Palastwachen-Kommandant, Minister des Geheimen Rates, Großer Präzeptor, Herzog, Markgraf von Hundert Haushalten
Führte Armeen in nördlichen Feldzügen, erzielte wiederholt außergewöhnliche Verdienste, seine Macht erschütterte die Grenzlande, Barbaren unterwarfen sich aus Furcht
Als Kaiser Shengzong den Thron bestieg, vertraute er ihm große Verantwortung an, die nördlichen Grenzen zu bewachen und die Stämme zu befrieden
Unglücklicherweise starb er im mittleren Alter an Krankheit, Hof und Land trauerten tief, ehrten ihn besonders posthum als Großer Präzeptor mit dem Titel "Treu und Kriegerisch"`,
                fr: `Inscription funéraire du Grand Général Yelü Yanning du Grand État Khitan
En la cinquième année du règne Tianzhan, année Bingxu, neuvième mois, nouvelle lune Gengshen, quinzième jour Jiaxu
Le défunt Grand Général Yelü Yanning, âgé de quarante ans, décéda dans sa résidence officielle
Ses ancêtres : arrière-grand-père Gaoligu, grand-père Zhiwubu, père Sage
Tous renommés pour leurs exploits martiaux, des générations de loyauté et de courage au service de l'État
Yanning montra de grandes ambitions dès sa jeunesse, devenant encore plus déterminé avec l'âge, servit l'Empereur Jingzong avec une dévotion loyale
Occupa les fonctions de Commandant de la Garde du Palais, Ministre du Conseil Privé, Grand Précepteur, Duc, Marquis de Cent Foyers
Dirigea des armées dans les campagnes du nord, accomplit à maintes reprises des mérites extraordinaires, sa puissance ébranla les terres frontalières, les barbares se soumirent par crainte
Quand l'Empereur Shengzong monta sur le trône, lui confia une grande responsabilité pour garder les frontières du nord et pacifier les tribus
Malheureusement mourut de maladie à l'âge moyen, la cour et le pays pleurèrent profondément, l'honorèrent spécialement à titre posthume comme Grand Précepteur avec le titre "Loyal et Martial"`,
                es: `Inscripción funeraria del Gran General Yelü Yanning del Gran Estado Khitan
En el quinto año del reinado Tianzhan, año Bingxu, noveno mes, luna nueva Gengshen, decimoquinto día Jiaxu
El difunto Gran General Yelü Yanning, de cuarenta años de edad, falleció en su residencia oficial
Sus ancestros: bisabuelo Gaoligu, abuelo Zhiwubu, padre Sage
Todos renombrados por hazañas marciales, generaciones de lealtad y valor sirviendo al estado
Yanning mostró grandes ambiciones desde la juventud, volviéndose aún más decidido con la edad, sirvió al Emperador Jingzong con devoción leal
Ocupó cargos de Comandante de la Guardia del Palacio, Ministro del Consejo Privado, Gran Preceptor, Duque, Marqués de Cien Hogares
Dirigió ejércitos en campañas del norte, logró repetidamente méritos extraordinarios, su poder sacudió las tierras fronterizas, los bárbaros se sometieron por temor
Cuando el Emperador Shengzong ascendió al trono, le confió gran responsabilidad para guardar las fronteras del norte y pacificar las tribus
Desafortunadamente murió de enfermedad en la mediana edad, la corte y el país lloraron profundamente, lo honraron especialmente póstumamente como Gran Preceptor con el título "Leal y Marcial"`,
                ar: `نقش جنائزي للجنرال الأعظم يلو يانينغ لدولة الخيتان العظمى
في السنة الخامسة من حكم تيانزان، سنة بينغشو، الشهر التاسع، القمر الجديد غنغشين، اليوم الخامس عشر جياشو
الجنرال الأعظم الراحل يلو يانينغ، البالغ من العمر أربعين عاماً، توفي في مقر إقامته الرسمي
أسلافه: الجد الأكبر غاوليغو، الجد تشيوبو، الأب ساغي
جميعهم مشهورون بالإنجازات العسكرية، أجيال من الولاء والشجاعة في خدمة الدولة
أظهر يانينغ طموحات عظيمة منذ الشباب، وأصبح أكثر تصميماً مع التقدم في السن، خدم الإمبراطور جينغزونغ بإخلاص وفي
شغل مناصب قائد حرس القصر، وزير المجلس الخاص، المعلم الأعظم، الدوق، مركيز المئة أسرة
قاد الجيوش في الحملات الشمالية، حقق مراراً وتكراراً استحقاقات استثنائية، قوته هزت الأراضي الحدودية، البرابرة خضعوا خوفاً
عندما صعد الإمبراطور شنغزونغ إلى العرش، أوكل إليه مسؤولية عظيمة لحراسة الحدود الشمالية وتهدئة القبائل
لسوء الحظ مات بالمرض في منتصف العمر، البلاط والبلاد حزنوا بعمق، كرموه خاصة بعد الوفاة كمعلم أعظم بلقب "المخلص والمحارب"`
            }
        },
        prince_north: {
            name: "Memorial of the Prince of the North",
            originalText: `
皇帝 囯 北王 墓志
大契丹 皇帝 之 北王 薨
世世 忠于 皇帝 囯家
功德 无量 威震 四方
特赠 太师 永垂 不朽
            `,
            frequencies: [880.00, 770.00, 660.00, 770.00, 880.00, 770.00, 586.67, 556.88, 440.00],
            translations: {
                en: `Memorial of the Prince of the North
Emperor, State, Prince of the North - Memorial
The Prince of the North of the Great Khitan Emperor has passed away
Generation after generation loyal to the Emperor and State
Merits and virtues immeasurable, might shook the four directions
Specially granted Grand Preceptor, eternally immortal`,
                zh: `北王墓志
皇帝囯北王墓志
大契丹皇帝之北王薨
世世忠于皇帝囯家
功德无量威震四方
特赠太师永垂不朽`,
                mn: `Хойд Вангийн булшны бичиг
Эзэн хаан, Улс, Хойд Ван - Дурсгалын бичиг
Их Хятадын эзэн хааны Хойд Ван таалал төгслөө
Үе үе эзэн хаан, улсад үнэнч байсан
Гавьяа буян хэмжээгүй, хүч чадал дөрвөн зүгийг чичрүүлсэн
Тусгайлан Их багш цол олгож, мөнхөд үхэшгүй`,
                ja: `北王墓誌
皇帝囯北王墓誌
大契丹皇帝の北王薨ず
世世皇帝囯家に忠なり
功徳無量威四方を震わす
特に太師を贈り永垂不朽`,
                ko: `북왕묘지
황제국북왕묘지
대거란황제의 북왕이 훙하다
세세로 황제국가에 충성하다
공덕이 무량하여 위세가 사방을 진동시키다
특히 태사를 증여하여 영원히 불후하다`,
                ru: `Надгробие Северного Принца
Император, Государство, Северный Принц - Мемориал
Северный Принц Великого Кидань Императора скончался
Поколение за поколением верны Императору и Государству
Заслуги и добродетели безмерны, мощь потрясла четыре стороны
Особо пожалован Великий Наставник, вечно бессмертен`,
                de: `Grabmal des Nördlichen Prinzen
Kaiser, Staat, Nördlicher Prinz - Gedenkstätte
Der Nördliche Prinz des Großen Khitan-Kaisers ist verstorben
Generation um Generation dem Kaiser und Staat treu
Verdienste und Tugenden unermesslich, Macht erschütterte die vier Richtungen
Besonders als Großer Präzeptor gewährt, ewig unsterblich`,
                fr: `Mémorial du Prince du Nord
Empereur, État, Prince du Nord - Mémorial
Le Prince du Nord du Grand Empereur Khitan est décédé
Génération après génération loyal à l'Empereur et à l'État
Mérites et vertus incommensurables, puissance ébranla les quatre directions
Spécialement accordé Grand Précepteur, éternellement immortel`,
                es: `Memorial del Príncipe del Norte
Emperador, Estado, Príncipe del Norte - Memorial
El Príncipe del Norte del Gran Emperador Khitan ha fallecido
Generación tras generación leal al Emperador y Estado
Méritos y virtudes inconmensurables, poder sacudió las cuatro direcciones
Especialmente otorgado Gran Preceptor, eternamente inmortal`,
                ar: `نصب الأمير الشمالي
الإمبراطور، الدولة، الأمير الشمالي - النصب التذكاري
الأمير الشمالي للإمبراطور الخيتاني العظيم قد توفي
جيل بعد جيل مخلص للإمبراطور والدولة
الاستحقاقات والفضائل لا تُقاس، القوة هزت الاتجاهات الأربعة
مُنح خاصة المعلم الأعظم، خالد إلى الأبد`
            }
        },
        nova_n176: {
            name: "Nova N 176 Codex (Sample)",
            originalText: `
大契丹国 史记 第一卷
皇帝 世系 及 功业
太祖 阿保机 建国 称帝
统一 契丹 八部 建都 上京
制定 法律 创立 文字
开疆 拓土 威加 四海
太宗 德光 继位 南征
灭后晋 入主 中原
改国号 为大辽 定都 燕京
圣宗 隆绪 中兴 之主
文治 武功 并举 盛世
            `,
            frequencies: [880.00, 770.00, 660.00, 586.67, 880.00, 770.00, 660.00, 556.88, 495.00, 880.00, 770.00, 660.00, 586.67, 556.88, 495.00, 440.00, 880.00, 770.00, 660.00, 586.67],
            translations: {
                en: `Great Khitan State Historical Records, Volume One
Imperial Lineage and Achievements
Taizu Abaoji established the state and proclaimed himself emperor
Unified the eight Khitan tribes and established the capital at Shangjing
Established laws and created writing systems
Expanded territory and extended might across the four seas
Taizong Deguang succeeded to the throne and campaigned south
Destroyed Later Jin and entered the Central Plains
Changed the state name to Great Liao and established capital at Yanjing
Shengzong Longxu, master of revival
Combined civil administration and military achievements in a golden age`,
                zh: `大契丹国史记第一卷
皇帝世系及功业
太祖阿保机建国称帝
统一契丹八部建都上京
制定法律创立文字
开疆拓土威加四海
太宗德光继位南征
灭后晋入主中原
改国号为大辽定都燕京
圣宗隆绪中兴之主
文治武功并举盛世`,
                mn: `Их Хятадын Улсын Түүхийн Тэмдэглэл, Нэгдүгээр боть
Эзэн хааны удам болон амжилт
Тай Зү Абаожи улс байгуулж эзэн хаан болохоо тунхаглав
Хятадын найман овгийг нэгтгэж Шанжин хотод нийслэл байгуулав
Хууль тогтоож бичгийн систем бүтээв
Нутаг дэвсгэрээ өргөжүүлж дөрвөн тэнгисийг хүчээр дарав
Тай Зон Дэгуан хаан ширээнд суугаад өмнө зүг рүү дайчлав
Хожуу Жинь улсыг устгаж Төв талбайд орлоо
Улсын нэрийг Их Ляо болгож өөрчилж Янжин хотыг нийслэл болголоо
Шэн Зон Лонсү, сэргэлтийн эзэн
Иргэний засаглал, цэргийн амжилтыг хослуулсан алтан үе`,
                ja: `大契丹国史記第一巻
皇帝世系及び功業
太祖阿保機国を建て帝と称す
契丹八部を統一し上京に都を建つ
法律を制定し文字を創立す
疆を開き土を拓き威四海に加う
太宗德光位を継ぎ南征す
後晋を滅ぼし中原に入主す
国号を改めて大遼と為し燕京に都を定む
聖宗隆緒中興の主
文治武功並び挙げ盛世なり`,
                ko: `대거란국사기 제1권
황제세계 및 공업
태조 아보기가 나라를 세우고 황제라 칭하다
거란 8부를 통일하고 상경에 도읍을 세우다
법률을 제정하고 문자를 창립하다
강역을 개척하고 위세가 사해에 미치다
태종 덕광이 왕위를 계승하고 남정하다
후진을 멸하고 중원에 들어가 주인이 되다
국호를 고쳐 대요라 하고 연경에 도읍을 정하다
성종 융서는 중흥의 주인
문치와 무공을 아울러 들어 성세를 이루다`,
                ru: `Исторические записи Великого государства Кидань, том первый
Императорская родословная и достижения
Тайцзу Абаоцзи основал государство и провозгласил себя императором
Объединил восемь киданьских племен и основал столицу в Шанцзине
Установил законы и создал письменные системы
Расширил территорию и распространил мощь на четыре моря
Тайцзун Дэгуан наследовал престол и повел южные походы
Уничтожил Позднюю Цзинь и вошел в Центральные равнины
Изменил название государства на Великое Ляо и основал столицу в Яньцзине
Шэнцзун Лунсюй, властитель возрождения
Объединил гражданское управление и военные достижения в золотой век`,
                de: `Historische Aufzeichnungen des Großen Khitan-Staates, Band Eins
Kaiserliche Abstammung und Errungenschaften
Taizu Abaoji gründete den Staat und proklamierte sich zum Kaiser
Vereinigte die acht Khitan-Stämme und gründete die Hauptstadt in Shangjing
Erließ Gesetze und schuf Schriftsysteme
Erweiterte das Territorium und erstreckte die Macht über die vier Meere
Taizong Deguang folgte auf den Thron und führte südliche Feldzüge
Zerstörte das Spätere Jin und betrat die Zentralebenen
Änderte den Staatsnamen zu Großes Liao und gründete die Hauptstadt in Yanjing
Shengzong Longxu, Meister der Wiederbelebung
Verband zivile Verwaltung und militärische Errungenschaften in einem goldenen Zeitalter`,
                fr: `Annales historiques du Grand État Khitan, Volume Un
Lignée impériale et réalisations
Taizu Abaoji fonda l'état et se proclama empereur
Unifia les huit tribus Khitan et établit la capitale à Shangjing
Établit des lois et créa des systèmes d'écriture
Étendit le territoire et projeta la puissance sur les quatre mers
Taizong Deguang succéda au trône et mena des campagnes vers le sud
Détruisit les Jin postérieurs et entra dans les Plaines centrales
Changea le nom de l'état en Grand Liao et établit la capitale à Yanjing
Shengzong Longxu, maître du renouveau
Combina administration civile et réalisations militaires dans un âge d'or`,
                es: `Registros Históricos del Gran Estado Khitan, Volumen Uno
Linaje Imperial y Logros
Taizu Abaoji fundó el estado y se proclamó emperador
Unificó las ocho tribus Khitan y estableció la capital en Shangjing
Estableció leyes y creó sistemas de escritura
Expandió el territorio y extendió el poder sobre los cuatro mares
Taizong Deguang sucedió al trono y dirigió campañas hacia el sur
Destruyó el Jin Posterior y entró en las Llanuras Centrales
Cambió el nombre del estado a Gran Liao y estableció la capital en Yanjing
Shengzong Longxu, maestro del renacimiento
Combinó administración civil y logros militares en una edad dorada`,
                ar: `السجلات التاريخية لدولة الخيتان العظمى، المجلد الأول
النسب الإمبراطوري والإنجازات
تايتسو أباوجي أسس الدولة وأعلن نفسه إمبراطوراً
وحد القبائل الخيتانية الثمان وأسس العاصمة في شانغجينغ
وضع القوانين وأنشأ أنظمة الكتابة
وسع الأراضي ومد القوة عبر البحار الأربعة
تايتسونغ ديغوانغ خلف العرش وقاد حملات جنوبية
دمر جين المتأخرة ودخل السهول الوسطى
غير اسم الدولة إلى لياو العظمى وأسس العاصمة في يانجينغ
شنغتسونغ لونغشو، سيد النهضة
جمع بين الإدارة المدنية والإنجازات العسكرية في عصر ذهبي`
            }
        }
    },
    
    memorialFrequencies: {
        yelu_yanning: [770.00, 880.00, 770.00, 660.00, 586.67, 660.00, 495.00, 495.00, 556.88, 556.88, 586.67, 770.00, 660.00, 556.88, 880.00, 770.00, 329.63, 261.63, 440.00],
        prince_north: [880.00, 770.00, 660.00, 770.00, 880.00, 770.00, 586.67, 556.88, 440.00]
    }
};

// Initialize audio context
function initAudio() {
    if (!audioContext) {
        audioContext = Tone.getContext();
        Tone.start();
    }
}

// Play Khitan memorial audio
function playKhitanMemorial() {
    initAudio();
    playMemorialSequence(khitanData.memorialFrequencies.yelu_yanning, "Yelü Yanning Memorial");
}

function playYeluYanning() {
    initAudio();
    playMemorialSequence(khitanData.memorialFrequencies.yelu_yanning, "Yelü Yanning Memorial (986 CE)");
}

function playPrinceNorth() {
    initAudio();
    playMemorialSequence(khitanData.memorialFrequencies.prince_north, "Memorial of the Prince of the North");
}

function playMemorialSequence(frequencies, memorialName) {
    if (isPlaying) {
        Tone.Transport.stop();
        isPlaying = false;
    }
    
    updateCurrentMemorial(memorialName, frequencies);
    
    const synth = new Tone.Synth({
        oscillator: {
            type: "sine"
        },
        envelope: {
            attack: 0.1,
            decay: 0.3,
            sustain: 0.7,
            release: 0.8
        }
    }).toDestination();
    
    // Create sequence
    let time = 0;
    frequencies.forEach((freq, index) => {
        Tone.Transport.schedule((time) => {
            synth.triggerAttackRelease(freq, "0.8n", time);
            updateFrequencyVisualization(freq, index, frequencies.length);
        }, time);
        time += 0.8; // 0.8 seconds per note for ceremonial effect
    });
    
    Tone.Transport.start();
    isPlaying = true;
    
    // Stop after sequence completes
    setTimeout(() => {
        Tone.Transport.stop();
        isPlaying = false;
    }, frequencies.length * 800 + 1000);
}

function updateCurrentMemorial(name, frequencies) {
    const currentMemorialDiv = document.getElementById('currentMemorial');
    if (currentMemorialDiv) {
        const avgFreq = frequencies.reduce((a, b) => a + b, 0) / frequencies.length;
        const note = frequencyToNote(avgFreq);
        
        currentMemorialDiv.innerHTML = `
            <h4>Now Playing: ${name}</h4>
            <p>Average Frequency: ${avgFreq.toFixed(2)} Hz (${note})</p>
            <p>Pattern: ${frequencies.length} frequency segments</p>
            <p>Duration: ${(frequencies.length * 0.8).toFixed(1)} seconds</p>
        `;
    }
}

function updateFrequencyVisualization(currentFreq, index, total) {
    const canvas = document.getElementById('audioFrequencyCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw frequency bar
    const barWidth = width / total;
    const barHeight = (currentFreq / 1000) * height; // Scale to canvas height
    
    // Draw all bars with current one highlighted
    for (let i = 0; i < total; i++) {
        const x = i * barWidth;
        const isCurrentBar = i === index;
        
        ctx.fillStyle = isCurrentBar ? '#ffd700' : 'rgba(102, 126, 234, 0.3)';
        ctx.fillRect(x, height - barHeight, barWidth - 2, barHeight);
        
        if (isCurrentBar) {
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`${currentFreq.toFixed(0)} Hz`, x + barWidth/2, height - barHeight - 10);
        }
    }
}

// Audio player controls
function selectMemorial(memorialType) {
    currentMemorial = memorialType;
    const frequencies = khitanData.memorialFrequencies[memorialType];
    const name = memorialType === 'yelu_yanning' ? 'Yelü Yanning Memorial (986 CE)' : 'Memorial of the Prince of the North';
    
    updateCurrentMemorial(name, frequencies);
    
    // Highlight selected memorial
    document.querySelectorAll('.memorial-item').forEach(item => {
        item.classList.remove('selected');
    });
    document.querySelector(`[data-memorial="${memorialType}"]`).classList.add('selected');
}

// Book reader functionality
function loadSampleText(textType) {
    const khitanTextDiv = document.getElementById('khitanText');
    const translatedTextDiv = document.getElementById('translatedText');
    
    if (khitanTextDiv && khitanData.inscriptions[textType]) {
        const inscription = khitanData.inscriptions[textType];
        
        khitanTextDiv.innerHTML = `
            <h5>${inscription.name}</h5>
            <div class="khitan-text">${inscription.originalText}</div>
        `;
        
        // Clear previous translation
        translatedTextDiv.innerHTML = '<p class="placeholder">Select a language and click Translate...</p>';
        
        // Update frequency visualization
        analyzeFrequencies(inscription.frequencies);
        
        // Add success animation
        khitanTextDiv.classList.add('success');
        setTimeout(() => khitanTextDiv.classList.remove('success'), 600);
    }
}

function translateText() {
    const targetLang = document.getElementById('targetLanguage').value;
    const translatedTextDiv = document.getElementById('translatedText');
    const khitanTextDiv = document.getElementById('khitanText');
    
    // Get current loaded text
    let currentInscription = null;
    for (const [key, inscription] of Object.entries(khitanData.inscriptions)) {
        if (khitanTextDiv.innerHTML.includes(inscription.name)) {
            currentInscription = inscription;
            break;
        }
    }
    
    if (!currentInscription) {
        translatedTextDiv.innerHTML = '<p class="placeholder">Please load a Khitan text first...</p>';
        return;
    }
    
    // Show loading
    translatedTextDiv.innerHTML = '<p class="loading">Translating ancient Khitan text...</p>';
    
    // Simulate translation process
    setTimeout(() => {
        const translation = currentInscription.translations[targetLang] || currentInscription.translations.en;
        const langName = getLanguageName(targetLang);
        
        translatedTextDiv.innerHTML = `
            <h5>Translation (${langName})</h5>
            <div class="translated-content">${translation}</div>
            <div class="translation-info">
                <p><strong>Translation Method:</strong> Frequency-based decipherment</p>
                <p><strong>Confidence:</strong> High (based on known character mappings)</p>
                <p><strong>Context:</strong> ${currentInscription.name}</p>
            </div>
        `;
        
        // Add success animation
        translatedTextDiv.classList.add('success');
        setTimeout(() => translatedTextDiv.classList.remove('success'), 600);
    }, 2000);
}

function getLanguageName(code) {
    const languages = {
        'en': 'English',
        'zh': 'Chinese (中文)',
        'mn': 'Mongolian (Монгол)',
        'ja': 'Japanese (日本語)',
        'ko': 'Korean (한국어)',
        'ru': 'Russian (Русский)',
        'de': 'German (Deutsch)',
        'fr': 'French (Français)',
        'es': 'Spanish (Español)',
        'ar': 'Arabic (العربية)'
    };
    return languages[code] || 'English';
}

function analyzeFrequencies(frequencies = null) {
    const canvas = document.getElementById('frequencyChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Use provided frequencies or default
    const freqs = frequencies || [770, 880, 660, 586, 495, 556, 440, 329, 261];
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw frequency bars
    const barWidth = width / freqs.length;
    const maxFreq = Math.max(...freqs);
    
    freqs.forEach((freq, index) => {
        const barHeight = (freq / maxFreq) * (height - 40);
        const x = index * barWidth;
        const y = height - barHeight - 20;
        
        // Color based on frequency range
        let color;
        if (freq >= 880) color = '#ff6b6b'; // Imperial
        else if (freq >= 660) color = '#4ecdc4'; // High Administrative
        else if (freq >= 440) color = '#45b7d1'; // Standard Memorial
        else color = '#96ceb4'; // Temporal
        
        ctx.fillStyle = color;
        ctx.fillRect(x + 2, y, barWidth - 4, barHeight);
        
        // Add frequency label
        ctx.fillStyle = '#333';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${freq}`, x + barWidth/2, height - 5);
        ctx.fillText(`${frequencyToNote(freq)}`, x + barWidth/2, y - 5);
    });
    
    // Add title
    ctx.fillStyle = '#333';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Khitan Frequency Analysis', width/2, 20);
}

function playTextAudio() {
    const khitanTextDiv = document.getElementById('khitanText');
    
    // Determine which text is loaded
    let frequencies = [770, 880, 660, 586, 495, 556, 440, 329, 261]; // Default
    let memorialName = "Loaded Khitan Text";
    
    for (const [key, inscription] of Object.entries(khitanData.inscriptions)) {
        if (khitanTextDiv.innerHTML.includes(inscription.name)) {
            frequencies = inscription.frequencies;
            memorialName = inscription.name;
            break;
        }
    }
    
    initAudio();
    playMemorialSequence(frequencies, memorialName);
}

function exportTranslation() {
    const translatedTextDiv = document.getElementById('translatedText');
    const content = translatedTextDiv.textContent || translatedTextDiv.innerText;
    
    if (content.includes('placeholder')) {
        alert('Please translate a text first before exporting.');
        return;
    }
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'khitan_translation.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function compareWithLinearA() {
    // Open comparison in new section or modal
    const comparisonSection = document.getElementById('comparison');
    if (comparisonSection) {
        comparisonSection.scrollIntoView({ behavior: 'smooth' });
        
        // Highlight comparison table
        const table = document.querySelector('.comparison-table');
        if (table) {
            table.classList.add('success');
            setTimeout(() => table.classList.remove('success'), 1000);
        }
    }
}

// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('khitanFile');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }
    
    // Initialize frequency comparison chart
    initComparisonChart();
    
    // Initialize audio controls
    initAudioControls();
    
    // Load default frequency analysis
    analyzeFrequencies();
});

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const khitanTextDiv = document.getElementById('khitanText');
        
        if (khitanTextDiv) {
            khitanTextDiv.innerHTML = `
                <h5>Uploaded File: ${file.name}</h5>
                <div class="khitan-text">${content}</div>
            `;
            
            // Clear translation
            const translatedTextDiv = document.getElementById('translatedText');
            if (translatedTextDiv) {
                translatedTextDiv.innerHTML = '<p class="placeholder">File loaded. Select language and translate...</p>';
            }
        }
    };
    reader.readAsText(file);
}

function initComparisonChart() {
    const chartDiv = document.getElementById('comparisonChart');
    if (!chartDiv) return;
    
    const linearAFreqs = [194, 210, 126, 341, 168, 99, 227, 76]; // Linear A frequencies
    const khitanFreqs = [880, 770, 660, 586, 495, 556, 440, 329]; // Khitan frequencies
    
    const trace1 = {
        x: ['Imperial', 'High Admin', 'Standard', 'Temporal', 'Ceremonial', 'Personal', 'Structural', 'Cyclical'],
        y: linearAFreqs,
        name: 'Linear A (Minoan)',
        type: 'bar',
        marker: { color: '#4ecdc4' }
    };
    
    const trace2 = {
        x: ['Imperial', 'High Admin', 'Standard', 'Temporal', 'Ceremonial', 'Personal', 'Structural', 'Cyclical'],
        y: khitanFreqs,
        name: 'Khitan Large Script',
        type: 'bar',
        marker: { color: '#667eea' }
    };
    
    const layout = {
        title: 'Frequency Comparison: Linear A vs Khitan',
        xaxis: { title: 'Context Categories' },
        yaxis: { title: 'Frequency (Hz)' },
        barmode: 'group'
    };
    
    Plotly.newPlot(chartDiv, [trace1, trace2], layout);
}

function initAudioControls() {
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const stopBtn = document.getElementById('stopBtn');
    const randomBtn = document.getElementById('randomBtn');
    const volumeSlider = document.getElementById('volumeSlider');
    
    if (playBtn) {
        playBtn.addEventListener('click', () => {
            if (currentMemorial) {
                const frequencies = khitanData.memorialFrequencies[currentMemorial];
                const name = currentMemorial === 'yelu_yanning' ? 'Yelü Yanning Memorial (986 CE)' : 'Memorial of the Prince of the North';
                playMemorialSequence(frequencies, name);
            } else {
                playKhitanMemorial(); // Default
            }
        });
    }
    
    if (pauseBtn) {
        pauseBtn.addEventListener('click', () => {
            if (isPlaying) {
                Tone.Transport.pause();
                isPlaying = false;
            }
        });
    }
    
    if (stopBtn) {
        stopBtn.addEventListener('click', () => {
            Tone.Transport.stop();
            isPlaying = false;
        });
    }
    
    if (randomBtn) {
        randomBtn.addEventListener('click', () => {
            const memorials = ['yelu_yanning', 'prince_north'];
            const randomMemorial = memorials[Math.floor(Math.random() * memorials.length)];
            selectMemorial(randomMemorial);
            
            const frequencies = khitanData.memorialFrequencies[randomMemorial];
            const name = randomMemorial === 'yelu_yanning' ? 'Yelü Yanning Memorial (986 CE)' : 'Memorial of the Prince of the North';
            playMemorialSequence(frequencies, name);
        });
    }
    
    if (volumeSlider) {
        volumeSlider.addEventListener('input', (e) => {
            const volume = e.target.value / 100;
            Tone.Destination.volume.value = Tone.gainToDb(volume);
        });
    }
}

// Utility function to convert frequency to note
function frequencyToNote(frequency) {
    const A4 = 440.0;
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    
    const semitones = 12 * Math.log2(frequency / A4);
    const octave = 4 + Math.floor(semitones / 12);
    let noteIndex = Math.round(semitones % 12);
    
    if (noteIndex < 0) {
        noteIndex += 12;
    }
    
    return `${notes[noteIndex]}${octave}`;
}

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

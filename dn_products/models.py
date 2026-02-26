from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.TextChoices):
    HS="hot_shower","Hot Shower"
    EX="extension","Extension"
    BT="battery","Batteries"
    ELT="electric_tester","Electric Tester"
    SPG="super_glue","Super Glue"
    BH="bulb_holder","Bulb Holder"
    WS="wall_socket","Wall Socket"
    FTG="fridge_tv_guard","Fridge/TV Guard"
    BLB="bulb","Bulbs"
    TR="tv_remote","TV Remotes"
    SHM="shaving_machine","Shaving Machine",
    WH="water_heater","Water Heater"
    GB="gas_burner","Gas Burner"
    SWC="smart_watch_charger","Smart Watch Chargers"
    TVB="tv_box","TV Box"
    TVA="tv_aerial","TV Aerial"
    PBR="phone_battery","Phone Battery"
    VC="video_cable","Video Cable"
    
    WFD="wifi_dongle","Wifi Dongle"
    BLD="bluetooth_dongle","Bluetooth Dongle"
    
    BTS="bluetooth_speaker","Bluetooth Speaker"
    
    
    
    SM="smart_phone","Smart Phone" #done
    FP="featured_phone","Featured Phone" #done
    PC="phone_charger","Phone Charger" #done
    PHC="phone_casing","Phone Casing" #done
    MR="memory_card","Memory Card" # done
    FD="flash_disk","Flash Disk" # done
    HDD="hard_disk","Hard Disk Drive" # done
    SSD="ss_disk","Solid State Drive" # done
    RT="router","Router" # done
    CM="computer_mouse","Computer Mouse" # done
    CK="computer_keyboard","Computer Keyboard" #done
    MSC="music_system","Music System" #done
    TV="flat_screen_tv", "Flat Screen TV" #done
    PB="power_bank","Power Bank" #done
    DC="data_cable","Data Cable" # done
    SP="screen_protector","Screen Protector" # done
    EP="headPhones_and_earPhones","Earphones/Earbuds/Headphone"# done
    SMT="smart_watch", "Smart Watch" # done

category_groups = {
    "Phones": {
        ProductCategory.SM.value: ProductCategory.SM.label,
        ProductCategory.FP.value: ProductCategory.FP.label,
    },
    "Storage": {
        ProductCategory.MR.value: ProductCategory.MR.label,
        ProductCategory.FD.value: ProductCategory.FD.label,
        ProductCategory.HDD.value: ProductCategory.HDD.label,
        ProductCategory.SSD.value: ProductCategory.SSD.label,
    },
    "Phone Accessories": {
        ProductCategory.PC.value: ProductCategory.PC.label,
        ProductCategory.PHC.value: ProductCategory.PHC.label,
        ProductCategory.DC.value: ProductCategory.DC.label,
        ProductCategory.SP.value: ProductCategory.SP.label,
        ProductCategory.PB.value: ProductCategory.PB.label,
        ProductCategory.EP.value: ProductCategory.EP.label,
        ProductCategory.SMT.value: ProductCategory.SMT.label,
        ProductCategory.SWC.value:ProductCategory.SWC.label,
        ProductCategory.PBR.value:ProductCategory.PBR.label
    },
    "Computer Peripherals": {
        ProductCategory.CM.value: ProductCategory.CM.label,
        ProductCategory.CK.value: ProductCategory.CK.label,
        ProductCategory.VC.value:ProductCategory.VC.label
    },
    "Home Electronics": {
        ProductCategory.MSC.value: ProductCategory.MSC.label,
        ProductCategory.TV.value: ProductCategory.TV.label,
        ProductCategory.TR.value: ProductCategory.TR.label,
        ProductCategory.BTS.value:ProductCategory.BTS.label,
        ProductCategory.TVB.value:ProductCategory.TVB.label,
        ProductCategory.TVA.value:ProductCategory.TVA.label,
    },
    "Networking":{
        ProductCategory.RT.value: ProductCategory.RT.label,
        ProductCategory.WFD.value:ProductCategory.WFD.label,
        ProductCategory.BLD.value:ProductCategory.BLD.label
    },
    "Electrical & Lighting": {
        ProductCategory.BLB.value: ProductCategory.BLB.label,
        ProductCategory.BH.value: ProductCategory.BH.label,
        ProductCategory.WS.value: ProductCategory.WS.label,
        ProductCategory.EX.value: ProductCategory.EX.label,
        ProductCategory.BT.value: ProductCategory.BT.label,
    },
    "Appliances & Hardware": {
        ProductCategory.HS.value: ProductCategory.HS.label,      # Hot Shower
        ProductCategory.FTG.value: ProductCategory.FTG.label,      # Fridge Guard
        ProductCategory.ELT.value: ProductCategory.ELT.label,    # Electric Tester
        ProductCategory.SPG.value: ProductCategory.SPG.label,    # super glue
        ProductCategory.SHM.value: ProductCategory.SHM.label,    # Shaving Machine
        ProductCategory.WH.value: ProductCategory.WH.label,      # Water Heater
        ProductCategory.GB.value: ProductCategory.GB.label,      # Gas Burner
        
    }
    
    
}
class ChargerTipType(models.TextChoices):
        ATC="atc","Type A to C"
        CTC="ctc","Type C to C"
        MUSB="musb","A to Micro USB"
        LT="lightning", "Lightning Port"

class ChargerPortType(models.TextChoices):
    TC="type c","Type C"
    MUSB="micro usb","Micro USB"
    LT="lightning", "Lightning Port"

    


class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_brand=models.CharField(max_length=50)
    product_buy_price=models.FloatField()
    product_sell_price=models.FloatField()
    product_discount=models.IntegerField(default=0)
    product_count=models.SmallIntegerField()
    restock_threshold=models.SmallIntegerField()
    product_attributes=models.JSONField(default=dict)
    product_category=models.CharField(max_length=30,choices=ProductCategory.choices,default=ProductCategory.SM)
    stocker=models.ForeignKey(User,related_name="stocker_%(class)s",on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)
    product_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    class Meta:
        abstract=True
        
    @property
    def className(self):
        return self.__class__.__name__
    def __str__(self):
        return f"{self.product_name} ({self.product_brand})"
    
    @property
    def productID(self):
        return str(self.product_id).replace("-","_")
    @property
    def display_fields(self):
        """Returns a dict of {Verbose Name: Value}, excluding PK and attributes."""
        excluded_fields = ['product_id', 'product_attributes',"pictures","product_category"]
        display_data = {}
        
        for field in self._meta.fields:
            if field.name not in excluded_fields:
                # field.verbose_name gets the human-readable label
                # .capitalize() ensures the first letter is uppercase
                label = field.verbose_name.capitalize()
                
                # Check if the field has choices (like product_category)
                # to get the readable label instead of the DB value
                if field.choices:
                    value = getattr(self, f'get_{field.name}_display')()
                else:
                    value = getattr(self, field.name)
    
                    
                display_data[label] = value
                
        return display_data
    
# PHONES
class SimType(models.TextChoices):
    SN="single","Single Sim (1)"
    DL="dual","Dual Sim (2)"
    TH="three","Tripple Sim (3)"
    QD="quad", "Quad Sim (4)"
class Phones(Product):
    charger_type=models.CharField(max_length=20,choices=ChargerPortType.choices,default=ChargerPortType.TC)
    battery_capacity=models.IntegerField()
    pictures=models.JSONField(default=list)
    sim_type=models.CharField(max_length=6,choices=SimType.choices,default=SimType.SN)

    class Meta:
        abstract=True
        

# smart phones types

class SmartPhoneBrands(models.TextChoices):
    APPLE = "APPLE", _("Apple")
    SAMSUNG = "SAMSUNG", _("Samsung")
    GOOGLE = "GOOGLE", _("Google")
    XIAOMI = "XIAOMI", _("Xiaomi")
    OPPO = "OPPO", _("Oppo")
    VIVO = "VIVO", _("Vivo")
    HUAWEI = "HUAWEI", _("Huawei")
    HONOR = "HONOR", _("Honor")
    
    # --- PERFORMANCE & SUB-BRANDS ---
    ONEPLUS = "ONEPLUS", _("OnePlus")
    REALME = "REALME", _("Realme")
    POCO = "POCO", _("Poco")
    IQOO = "IQOO", _("iQOO")
    REDMI = "REDMI", _("Redmi")
    NOTHING = "NOTHING", _("Nothing")
    MOTOROLA = "MOTOROLA", _("Motorola")
    
    # --- SPECIALIZED & GAMING ---
    ASUS = "ASUS", _("Asus")
    ROG = "ROG", _("ROG Phone")
    NUBIA = "NUBIA", _("Nubia")
    REDMAGIC = "REDMAGIC", _("Red Magic")
    BLACK_SHARK = "BLACK_SHARK", _("Black Shark")
    RAZER = "RAZER", _("Razer")
    SONY = "SONY", _("Sony")
    
    # --- TRANSSION GROUP (Emerging Markets) ---
    TECNO = "TECNO", _("Tecno")
    INFINIX = "INFINIX", _("Infinix")
    ITEL = "ITEL", _("Itel")
    
    # --- REGIONAL & BUDGET ---
    NOKIA = "NOKIA", _("Nokia")
    HMD = "HMD", _("HMD")
    LAVA = "LAVA", _("Lava")
    MICROMAX = "MICROMAX", _("Micromax")
    JIO = "JIO", _("Jio")
    BLU = "BLU", _("BLU")
    WIKO = "WIKO", _("Wiko")
    ALCATEL = "ALCATEL", _("Alcatel")
    TCL = "TCL", _("TCL")
    ZTE = "ZTE", _("ZTE")
    MEIZU = "MEIZU", _("Meizu")
    
    # --- RUGGED & NICHE ---
    CAT = "CAT", _("Cat")
    BLACKVIEW = "BLACKVIEW", _("Blackview")
    DOOGEE = "DOOGEE", _("Doogee")
    ULEFONE = "ULEFONE", _("Ulefone")
    UMIDIGI = "UMIDIGI", _("Umidigi")
    FAIRPHONE = "FAIRPHONE", _("Fairphone")
    UNIHERTZ = "UNIHERTZ", _("Unihertz")
    
    # --- LEGACY / INACTIVE ---
    LG = "LG", _("LG")
    HTC = "HTC", _("HTC")
    BLACKBERRY = "BLACKBERRY", _("BlackBerry")
    LENOVO = "LENOVO", _("Lenovo")
    SHARP = "SHARP", _("Sharp")
    KYOCERA = "KYOCERA", _("Kyocera")
    PANASONIC = "PANASONIC", _("Panasonic")
    
    OTHER = "OTHER", _("Other")


class SmartPhone(Phones):
    product_brand=models.CharField(max_length=25,choices=SmartPhoneBrands.choices,default=SmartPhoneBrands.SAMSUNG)
    product_category=models.CharField(default=ProductCategory.SM)
    screen_size=models.FloatField()
    ram=models.IntegerField()
    rom=models.IntegerField(verbose_name="Internal Storage")
    
    def __str__(self):
        return f"{self.product_name} -{self.product_count}"

class FeaturePhoneBrands(models.TextChoices):
    NOKIA = "Nokia", "Nokia"
    ITEL = "Itel", "Itel"
    TECNO = "Tecno", "Tecno"
    SAMSUNG = "Samsung", "Samsung"
    LAVA = "Lava", "Lava"
    FERO = "Fero", "Fero"
    XTIGI = "X-Tigi", "X-Tigi"
    ALCATEL = "Alcatel", "Alcatel"
    ZTE = "ZTE", "ZTE"
    HUAWEI = "Huawei", "Huawei"
class FeaturedPhone(Phones):
    product_brand=models.CharField(choices=FeaturePhoneBrands.choices,max_length=25,default=FeaturePhoneBrands.TECNO)
    product_category=models.CharField(default=ProductCategory.FP)



class IMEI(models.Model):
    class Meta:
        abstract=True
    imei_list=models.JSONField(default=dict)

class SIMEI(IMEI):
    smartphone=models.ForeignKey(SmartPhone,related_name="phone_imeis",on_delete=models.CASCADE)

class FIME(IMEI):
    featuredphone=models.ForeignKey(FeaturedPhone,related_name="fphone_imeis",on_delete=models.CASCADE)

# MOBILE ACCESSORIES
# powerbank, charger, data-cable, screen protector, earbuds, headphones, 
class PhoneAccessories(Product):
    class Meta:
        abstract=True


class PowerBank(PhoneAccessories):
    class PowerBankBrand(models.TextChoices):
        # --- Kenyan Market Leaders ---
        ORAIMO = "ORAIMO", _("Oraimo")             # Dominant in local shops
        ANKER = "ANKER", _("Anker")               # Premium choice (Zolo/Prime series)
        XIAOMI = "XIAOMI", _("Xiaomi / Redmi")     # Very popular for sleek designs
        BASEUS = "BASEUS", _("Baseus")             # Known for high-wattage/laptop banks
        
        # --- Specialized & Emerging ---
        PRO_MATE = "PROMATE", _("Promate")         # Often found in electronics stores
        WOPOW = "WOPOW", _("Wopow")               # Popular budget "Container" designs
        POWEROLOGY = "POWEROLOGY", _("Powerology") # High-end smart display models
        ECOFLOW = "ECOFLOW", _("EcoFlow")         # For ultra-high capacity/power stations
        
        # --- Other Notable Brands ---
        ROMOSS = "ROMOSS", _("Romoss")
        SAMSUNG = "SAMSUNG", _("Samsung Official")
        REALME = "REALME", _("Realme")
        GENERIC = "GENERIC", _("Generic / No Brand")
        
        OTHER = "OTHER", _("Other")
    product_category=models.CharField(default=ProductCategory.PB)
    product_brand=models.CharField(max_length=50,choices=PowerBankBrand.choices,default=PowerBankBrand.ORAIMO)
    capacity=models.IntegerField()
# chargers
class ChargerBrands(models.TextChoices):
    APPLE = "apple", "Apple"
    SAMSUNG = "samsung", "Samsung"
    HUAWEI = "huawei", "Huawei"
    XIAOMI = "xiaomi", "Xiaomi"
    OPPO = "oppo", "Oppo"
    VIVO = "vivo", "Vivo"
    NOKIA = "nokia", "Nokia"
    SONY = "sony", "Sony"

    # Popular accessory brands
    ANKER = "anker", "Anker"
    AUKEY = "aukey", "Aukey"
    BASEUS = "baseus", "Baseus"
    BELKIN = "belkin", "Belkin"
    UGREEN = "ugreen", "Ugreen"
    ORAIMO = "oraimo", "Oraimo"
    INFINIX = "infinix", "Infinix"
    TECNO = "tecno", "Tecno"
    VITRON = "vitron", "Vitron"
    VISION_PLUS = "vision_plus", "Vision Plus" 

    # Catch-all
    GENERIC = "generic", "Generic/Universal"
    OTHER = "other", "Other / Unlisted"
class PhoneCharger(PhoneAccessories):
    
    class ChargerType(models.TextChoices):
        COMPLETE="COMPLETE",_("Complete")
        HEADER="HEADER",_("Header Only")
    product_category=models.CharField(default=ProductCategory.PC)
    product_brand=models.CharField(max_length=20,choices=ChargerBrands.choices,default=ChargerBrands.ORAIMO)
    charging_port=models.CharField(max_length=10,choices=ChargerTipType.choices,default=ChargerTipType.ATC)
    charger_type=models.CharField(max_length=15,choices=ChargerType.choices,default=ChargerType.COMPLETE)
    

class DataCable(PhoneAccessories):
    class Brand(models.TextChoices):
        # Mobile & Consumer Electronics (Common in retail shops)
        ORAIMO = 'ORM', _('Oraimo')
        EXCELLENT = 'EXL', _('Excellent')
        AWEI = 'AWE', _('Awei')
        ANKER = 'ANK', _('Anker')
        UGREEN = 'UGN', _('Ugreen')
        CELEBRAT = 'CEL', _('Celebrat')
        BASEUS = 'BAS', _('Baseus')
        ITEL = 'ITL', _('Itel')

        # Networking & Infrastructure (Common in Computer World/Nairobi CBD)
        SIEMON = 'SIE', _('Siemon')
        GIGANET = 'GIG', _('Giganet')
        DLINK = 'DLK', _('D-Link')
        HIKVISION = 'HIK', _('Hikvision')
        EASENET = 'ESN', _('EaseNet')
        MERCURY = 'MER', _('Mercury')
        
        # Local & Regional Manufacturers
        EA_CABLES = 'EAC', _('East African Cables')
        METSEC = 'MET', _('Metsec')
        
        # Specialized/Other
        VITRON = 'VIT', _('Vitron')
        GENERIC = 'GEN', _('Generic / Unbranded')
    product_category=models.CharField(default=ProductCategory.DC)
    product_brand=models.CharField(max_length=20,choices=Brand.choices,default=ChargerBrands.ORAIMO)
    cable_type=models.CharField(choices=ChargerTipType.choices,max_length=20,default=ChargerTipType.ATC)
    length=models.SmallIntegerField()
     

class AudioBrand(models.TextChoices):
    # Dominant Regional Brands
    ORAIMO = "ORAIMO", _("Oraimo")  # Market leader in Sub-Saharan Africa
    INFINIX = "INFINIX", _("Infinix")
    TECNO = "TECNO", _("Tecno")
    PROMATE = "PROMATE", _("Promate")
    
    # Established Global Brands (High African Presence)
    JBL = "JBL", _("JBL")
    SONY = "SONY", _("Sony")
    SAMSUNG = "SAMSUNG", _("Samsung")
    APPLE = "APPLE", _("Apple")
    ANKER = "ANKER", _("Anker Soundcore")
    
    # Premium / Audiophile Favorites
    BOSE = "BOSE", _("Bose")
    SENNHEISER = "SENNHEISER", _("Sennheiser")
    BEATS = "BEATS", _("Beats by Dre")
    
    # Emerging & Budget-Friendly
    PACE = "PACE", _("Pace")  # Kenyan homegrown brand
    VENTION = "VENTION", _("Vention")
    UGREEN = "UGREEN", _("UGreen")
    NOTHING = "NOTHING", _("Nothing/CMF")
    HIRE = "GENERIC", _("Other/Generic")
class HeadphonesAndEarphones(PhoneAccessories):
    class EType(models.TextChoices):
        HP="Head Phone","Head Phone"
        EP="Ear Phone","Ear Phone"
        EB="Ear Bud","Ear Bud"
        HD="Neck Headset","Neck Headset"
    class CType(models.TextChoices):
        AUX="AUX","AUX"
        TC="TC","Type C"
        NONE="NONE","None"
    product_category=models.CharField(default=ProductCategory.EP)
    product_brand=models.CharField(max_length=30,choices=AudioBrand.choices,default=AudioBrand.ORAIMO)
    e_type=models.CharField(choices=EType.choices,max_length=20,default=EType.EB)
    bluetooth=models.BooleanField(default=False)
    wired=models.BooleanField(default=True)
    c_type=models.CharField(max_length=20,choices=CType.choices,verbose_name="Connection Type",null=True,default=CType.AUX)


class ScreenProtectorBrand(models.TextChoices):
    # --- Kenyan Market Leaders ---
    ORAIMO = "ORAIMO", _("Oraimo")
    LITO = "LITO", _("Lito")
    MIETUBL = "MIETUBL", _("Mietubl")
    X_LEVEL = "XLEVEL", _("X-Level")
    
    # --- Popular Mid-Range / Imports ---
    SPIGEN = "SPIGEN", _("Spigen")
    ESR = "ESR", _("ESR")
    GLASSOLOGY = "GLASSOLOGY", _("Glassology")
    CELEBRAT = "CELEBRAT", _("Celebrat")
    ASTRUM = "ASTRUM", _("Astrum")
    
    # --- Specialized & Tablet ---
    PAPERLIKE = "PAPERLIKE", _("Paperlike")
    PANZERGLASS = "PANZERGLASS", _("PanzerGlass")
    
    # --- Generic / Market Names ---
    OG = "OG", _("OG / King Kong")
    BUFF = "BUFF", _("Buff")
    GENERIC = "GENERIC", _("Generic / No Brand")
    
    OTHER = "OTHER", _("Other")
    
class ScreenProtector(PhoneAccessories):
    product_subcategory=models.CharField(default="Screen Protector")
    product_brand=models.CharField(max_length=50,choices=ScreenProtectorBrand.choices,default=ScreenProtectorBrand.OG)
    phone_brand=models.CharField(max_length=50,choices=SmartPhoneBrands.choices,default=SmartPhoneBrands.TECNO)
    compatible_phones=models.JSONField(list)
    
    
class CaseBrand(models.TextChoices):
    # --- Major Players in Kenya ---
    ORAIMO = "ORAIMO", _("Oraimo")
    X_LEVEL = "XLEVEL", _("X-Level")
    LITO = "LITO", _("Lito")
    CELEBRAT = "CELEBRAT", _("Celebrat")
    ROAR_KOREA = "ROAR", _("Roar Korea")
    
    # --- Global Premium Brands ---
    SPIGEN = "SPIGEN", _("Spigen")
    OTTERBOX = "OTTERBOX", _("OtterBox")
    UAG = "UAG", _("UAG (Urban Armor Gear)")
    CASETIFY = "CASETIFY", _("Casetify")
    RINGKE = "RINGKE", _("Ringke")
    APPLE = "APPLE", _("Apple Official")
    SAMSUNG = "SAMSUNG", _("Samsung Official")
    
    # --- Budget & Common Generic Types ---
    SILICON = "SILICON", _("Generic Silicon / Jelly")
    LEATHER_FLIP = "FLIP", _("Generic Leather Flip")
    SHOCKPROOF = "SHOCK", _("Generic Shockproof / Armor")
    
    OTHER = "OTHER", _("Other")

class PhoneCasing(PhoneAccessories):
    product_subcategory=models.CharField(default="Phone Casing",editable=False)
    product_brand=models.CharField(max_length=50,choices=CaseBrand.choices,default=CaseBrand.ORAIMO)
    phone_brand=models.CharField(max_length=50,choices=SmartPhoneBrands.choices,default=SmartPhoneBrands.TECNO)
    phone_model=models.CharField(max_length=100)


# Electronics
class Electronics(Product):
    bluetooth=models.BooleanField(default=True)
    serial_no=models.CharField(max_length=100)
    model_no=models.CharField(max_length=100)
    class Meta:
        abstract=True


# music systems
class MusicHiFiBrands(models.TextChoices):
    SONY = "sony", "Sony"
    BOSE = "bose", "Bose"
    YAMAHA = "yamaha", "Yamaha"
    DENON = "denon", "Denon"
    ONKYO = "onkyo", "Onkyo"
    PIONEER = "pioneer", "Pioneer"
    MARANTZ = "marantz", "Marantz"
    HARMAN_KARDON = "harman_kardon", "Harman Kardon"
    JBL = "jbl", "JBL"
    KLIPSCH = "klipsch", "Klipsch"
    BOWERS_WILKINS = "bowers_wilkins", "Bowers & Wilkins"
    KEF = "kef", "KEF"
    CAMBRIDGE_AUDIO = "cambridge_audio", "Cambridge Audio"
    NAD = "nad", "NAD"
    TECHNICS = "technics", "Technics"
    PANASONIC = "panasonic", "Panasonic"
    SAMSUNG = "samsung", "Samsung"
    LG = "lg", "LG"
    PHILIPS = "philips", "Philips"
    SONOS = "sonos", "Sonos"
    DEVIALET = "devialet", "Devialet"
    FOCAL = "focal", "Focal"
    AKAI = "akai", "Akai"
    TEAC = "teac", "TEAC"
    SHARP = "sharp", "Sharp"
    SANYO = "sanyo", "Sanyo"
    JVC = "jvc", "JVC"
    
    # Local/Regional Brands
    VITRON = "vitron", "Vitron"
    VISION_PLUS = "vision_plus", "Vision Plus"

    # Catch-all option
    OTHER = "other", "Other / Unlisted"
    
    
class MusicSystem(Electronics):
    class SystemType(models.TextChoices):
        HIFI="HIFI","Hi-Fi System"
        SB="SB","Sound Bar"
    product_brand=models.CharField(default=MusicHiFiBrands.SANYO,choices=MusicHiFiBrands.choices)
    product_category=models.CharField(default=ProductCategory.MSC)
    channel=models.IntegerField()
    watts=models.IntegerField()
    system_type=models.CharField(max_length=4,choices=SystemType.choices,verbose_name="Type",default=SystemType.HIFI)
# TVS

class TVBrands(models.TextChoices):
    VITRON = "vitron", "Vitron"
    SAMSUNG = "samsung", "Samsung"
    LG = "lg", "LG"
    SONY = "sony", "Sony"
    PANASONIC = "panasonic", "Panasonic"
    TOSHIBA = "toshiba", "Toshiba"
    HISENSE = "hisense", "Hisense"
    TCL = "tcl", "TCL"
    PHILIPS = "philips", "Philips"
    SHARP = "sharp", "Sharp"
    VIZIO = "vizio", "Vizio"
    MI = "mi", "Xiaomi / Mi"
    ONEPLUS = "oneplus", "OnePlus"
    HAIER = "haier", "Haier"
    SKYWORTH = "skyworth", "Skyworth"
    INSIGNIA = "insignia", "Insignia"
    HITACHI = "hitachi", "Hitachi"
    SANYO = "sanyo", "Sanyo"
    GRUNDIG = "grundig", "Grundig"
    JVC = "jvc", "JVC"
    PIONEER = "pioneer", "Pioneer"
    RCA = "rca", "RCA"
    WESTINGHOUSE = "westinghouse", "Westinghouse"
    ELEMENT = "element", "Element"
    KONKA = "konka", "Konka"
    POLAROID = "polaroid", "Polaroid"
    MAGNAVOX = "magnavox", "Magnavox"
    SEIKI = "seiki", "Seiki"
    OTHERS="Others","Others"

class FlatScreenTv(Electronics):
    class Resolution(models.TextChoices):
        FHD="FHD","Full HD"
        UHD="UHD","Ultra HD"    
    class TVType(models.TextChoices):
        SMT="Smart","Smart TV"
        DGT="Digital", "Digital TV"
    product_brand=models.CharField(default=TVBrands.SAMSUNG,choices=TVBrands.choices)
    product_category=models.CharField(default=ProductCategory.TV,editable=False)
    inches=models.IntegerField()
    resolution=models.CharField(max_length=10,choices=Resolution.choices,default=Resolution.FHD)
    frameless=models.BooleanField(default=False)
    tv_type=models.CharField(choices=TVType.choices,max_length=7,default=TVType.SMT)

class SmartwatchBrand(models.TextChoices):
        APPLE = "apple", "Apple"
        SAMSUNG = "samsung", "Samsung"
        GARMIN = "garmin", "Garmin"
        HUAWEI = "huawei", "Huawei"
        FITBIT = "fitbit", "Fitbit"
        XIAOMI = "xiaomi", "Xiaomi"
        AMAZFIT = "amazfit", "Amazfit"
        ORAIMO = "oraimo", "Oraimo"
        ITEL = "itel", "itel"
        HAVIT = "havit", "Havit"
        OTHER = "other", "Other / Generic"
class SmartWatch(Product):
    class SmartwatchShape(models.TextChoices):
        SQUARE = "square", "Square"
        CIRCLE = "circle", "Circle"
        RECTANGLE = "rectangle", "Rectangle"
    class Compatibility(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"
        BOTH = "both", "Android & iOS"
    product_brand=models.CharField(max_length=20,default=SmartwatchBrand.ORAIMO,choices=SmartwatchBrand.choices)
    product_category=models.CharField(max_length=20,default=ProductCategory.SMT,editable=False)
    amoled_screen=models.BooleanField(default=False)
    form_factor=models.CharField(max_length=15,choices=SmartwatchShape.choices,default=SmartwatchShape.CIRCLE)
    is_rugged=models.BooleanField(default=False)
    compatibility=models.CharField(max_length=20,choices=Compatibility.choices,default=Compatibility.BOTH)
    
class StorageBrand(models.TextChoices):
    # --- The "Big Three" Manufacturers (NAND/DRAM) ---
    SANDISK = "SANDISK", _("SanDisk / Western Digital")
    SAMSUNG = "SAMSUNG", _("Samsung")
    MICRON = "MICRON", _("Micron / Crucial")
    SK_HYNIX = "SK_HYNIX", _("SK Hynix / Solidigm")
    
    # --- Major Global Flash & SSD Brands ---
    KINGSTON = "KINGSTON", _("Kingston")
    PNY = "PNY", _("PNY")
    ADATA = "ADATA", _("ADATA / XPG")
    LEXAR = "LEXAR", _("Lexar")
    TRANSCEND = "TRANSCEND", _("Transcend")
    SEAGATE = "SEAGATE", _("Seagate")
    
    # --- High-Performance RAM & Enthusiast Brands ---
    CORSAIR = "CORSAIR", _("Corsair")
    GSKILL = "GSKILL", _("G.Skill")
    TEAMGROUP = "TEAMGROUP", _("TeamGroup / T-Force")
    SABRENT = "SABRENT", _("Sabrent")
    PATRIOT = "PATRIOT", _("Patriot / Viper")
    MUSHKIN = "MUSHKIN", _("Mushkin")
    
    # --- Regional & Budget Brands ---
    INTENSO = "INTENSO", _("Intenso")
    HP = "HP", _("HP (Licensed by Biwin)")
    NETAC = "NETAC", _("Netac")
    HIKVISION = "HIKVISION", _("Hikvision")
    KIOXIA = "KIOXIA", _("Kioxia (formerly Toshiba)")
    
    OTHER = "OTHER", _("Other")
    
class Storage(Product):
    product_brand=models.CharField(max_length=50,verbose_name="Memory card brand",choices=StorageBrand.choices,default=StorageBrand.SANDISK)
    size=models.IntegerField(verbose_name="Memory card size in (GB)")
    
    class Meta:
        abstract=True
        
class MemoryCard(Storage):
    product_category=models.CharField(max_length=50,default=ProductCategory.MR,editable=False) 
    
class FlashDisk(Storage):
    product_category=models.CharField(max_length=50,default=ProductCategory.FD,editable=False)
class HardDisk(Storage):
    product_category=models.CharField(max_length=50,default=ProductCategory.HDD,editable=False)
class SsDisk(Storage):
    product_category=models.CharField(max_length=50,default=ProductCategory.SSD,editable=False)
    
    

# ROUTER
class RouterBrand(models.TextChoices):
    # --- Consumer Favorites ---
    TP_LINK = "TP_LINK", _("TP-Link")
    ASUS = "ASUS", _("ASUS")
    NETGEAR = "NETGEAR", _("Netgear")
    LINKSYS = "LINKSYS", _("Linksys")
    D_LINK = "D_LINK", _("D-Link")
    TEND_A = "TENDA", _("Tenda")
    MERCUSYS = "MERCUSYS", _("Mercusys")
    
    # --- Mesh Specialists ---
    EERO = "EERO", _("eero (Amazon)")
    GOOGLE = "GOOGLE", _("Google Nest")
    ORBI = "ORBI", _("Netgear Orbi")
    
    # --- High-End & Enterprise (SMB) ---
    UBIQUITI = "UBIQUITI", _("Ubiquiti (UniFi/AmpliFi)")
    MIKROTIK = "MIKROTIK", _("MikroTik")
    CISCO = "CISCO", _("Cisco")
    SYNOLOGY = "SYNOLOGY", _("Synology")
    GL_INET = "GL_INET", _("GL.iNet")
    
    # --- Mobile & Regional ---
    HUAWEI = "HUAWEI", _("Huawei")
    XIAOMI = "XIAOMI", _("Xiaomi")
    ZTE = "ZTE", _("ZTE")
    NOKIA = "NOKIA", _("Nokia")
    
    OTHER = "OTHER", _("Other")
class Router(Product):
    product_brand = models.CharField(max_length=20, choices=RouterBrand.choices,verbose_name="Router Brand")
    product_category=models.CharField(max_length=20,default=ProductCategory.RT)
    wifi_standard = models.CharField(
        max_length=20, 
        choices=[
            ("WIFI5", "Wi-Fi 5 (802.11ac)"),
            ("WIFI6", "Wi-Fi 6 (802.11ax)"),
            ("WIFI6E", "Wi-Fi 6E"),
            ("WIFI7", "Wi-Fi 7 (802.11be)"),
        ]
    )
    total_speed_mbps = models.PositiveIntegerField(help_text="Combined speed in Mbps",verbose_name="Total Speed in Mb/s")
    lan_ports_count = models.PositiveSmallIntegerField(default=4,verbose_name="Number of Ports")
    has_mesh_support = models.BooleanField(default=False)
    
    
    
# KEYBOARD MOUSE
class MouseBrand(models.TextChoices):
    # --- The Market Leaders ---
    LOGITECH = "LOGITECH", _("Logitech")
    RAZER = "RAZER", _("Razer")
    STEELSERIES = "STEELSERIES", _("SteelSeries")
    CORSAIR = "CORSAIR", _("Corsair")
    
    # --- High-Performance & Gaming Specialists ---
    GLORIOUS = "GLORIOUS", _("Glorious")
    ZOWIE = "ZOWIE", _("Zowie (BenQ)")
    ROCCAT = "ROCCAT", _("Roccat (Turtle Beach)")
    HYPERX = "HYPERX", _("HyperX")
    ASUS_ROG = "ASUS_ROG", _("ASUS ROG")
    FINALMOUSE = "FINALMOUSE", _("Finalmouse")
    LAMZU = "LAMZU", _("Lamzu")
    PULSAR = "PULSAR", _("Pulsar")

    # --- Productivity & Ergonomics ---
    MICROSOFT = "MICROSOFT", _("Microsoft / Surface")
    APPLE = "APPLE", _("Apple")
    HP = "HP", _("HP")
    DELL = "DELL", _("Dell")
    LENOVO = "LENOVO", _("Lenovo")
    KENSINGTON = "KENSINGTON", _("Kensington")
    ANKER = "ANKER", _("Anker")
    
    # --- Budget & Common OEM ---
    REDDRAGON = "REDDRAGON", _("Redragon")
    TRUST = "TRUST", _("Trust")
    A4TECH = "A4TECH", _("A4Tech / Bloody")
    GENIUS = "GENIUS", _("Genius")
    OTHER = "OTHER", _("Other")

class Connection(models.TextChoices):
        WIRED = "WIRED", _("Wired")
        WIRELESS = "WIRELESS", _("Wireless (2.4GHz)")
        BLUETOOTH = "BT", _("Bluetooth")
        TRI_MODE = "TRI", _("Tri-Mode (Wired/2.4G/BT)")

class ComputerMouse(Product):
    product_brand = models.CharField(max_length=20, choices=MouseBrand.choices,default=MouseBrand.HP,verbose_name="Mouse Brand")
    connection = models.CharField(max_length=10, choices=Connection.choices,default=Connection.WIRED)
    max_dpi = models.PositiveIntegerField(default=1600)
    is_programmable = models.BooleanField(default=False)

    
    
# COMPUTER KEYBOARD
class KeyboardBrand(models.TextChoices):
    # --- Major Global Brands ---
    LOGITECH = "LOGITECH", _("Logitech")
    RAZER = "RAZER", _("Razer")
    CORSAIR = "CORSAIR", _("Corsair")
    
    # --- Budget & High-Volume Manufacturers ---
    T_WOLF = "TWOLF", _("T-Wolf")  # Added here
    REDDRAGON = "REDDRAGON", _("Redragon")
    ROYAL_KLUDGE = "ROYAL_KLUDGE", _("Royal Kludge (RK)")
    AULA = "AULA", _("Aula")
    HAVIT = "HAVIT", _("Havit")
    METOO = "METOO", _("Metoo")
    
    # --- Productivity & Budget ---
    APPLE = "APPLE", _("Apple")
    MICROSOFT = "MICROSOFT", _("Microsoft")
    DELL = "DELL", _("Dell")
    HP = "HP", _("HP")
    LENOVO = "LENOVO", _("Lenovo")
    CHERRY = "CHERRY", _("Cherry")
    
    # --- Enthusiast Brands ---
    KEYCHRON = "KEYCHRON", _("Keychron")
    AKKO = "AKKO", _("Akko")
    
    OTHER = "OTHER", _("Other")
    

class ComputerKeyboard(Product):
    product_brand = models.CharField(max_length=20, choices=KeyboardBrand.choices,default=KeyboardBrand.HP,verbose_name="Keyboard Brand")
    class Size(models.TextChoices):
        FULL = "100", _("Full-size (104/108 keys)")
        TKL = "80", _("Tenkeyless (80%)")
        COMPACT_75 = "75", _("75%")
        COMPACT_65 = "65", _("65%")
        MINI = "60", _("60%")
    size = models.CharField(max_length=5, choices=Size.choices,default=Size.MINI)
    connection = models.CharField(max_length=50, choices=Connection.choices,default=Connection.WIRED)
    is_hotswappable = models.BooleanField(default=False)
    has_rgb = models.BooleanField(default=False)
    
    
    
# Hot Shower

class HotShower(Product):
    class HotShowerBrand(models.TextChoices):
        LORENZETTI = "lorenzetti", "Lorenzetti"
        ARISTON = "ariston", "Ariston"
        STIEBEL = "stiebel_eltron", "Stiebel Eltron"
        JOVEN = "joven", "Joven"
        ENVIRO = "enviro", "Enviro"
        OTHER = "other", "Other"
        
    class ControlType(models.TextChoices):
        FIXED = "fixed", "Fixed (Single Temp)"
        STEPPED = "stepped", "Stepped (e.g. Low/Med/High)"
        STEPLESS = "stepless", "Stepless (Electronic Dial)"
        DIGITAL = "digital", "Digital Touch"
    
    product_brand=models.CharField(max_length=30,choices=HotShowerBrand.choices,default=HotShowerBrand.LORENZETTI)
    product_category = models.CharField(max_length=30, default=ProductCategory.HS)
    wattage = models.IntegerField(help_text="Wattage in Watts (e.g., 5500)")
    control = models.CharField(
        max_length=20, 
        choices=ControlType.choices, 
        default=ControlType.STEPPED
    )
    
    
class Extension(Product):
    class ExtensionBrand(models.TextChoices):
        TRIONIC = "trionic", "Trionic"
        PREMIER = "premier", "Premier"
        APC = "apc", "APC"
        BULL = "bull", "Bull"
        GENERIC = "generic", "Generic"
        OTHER = "other", "Other"

    class Sockets(models.IntegerChoices):
        TWO_WAY = 2, "2-Way"
        THREE_WAY = 3, "3-Way"
        FOUR_WAY = 4, "4-Way"
        FIVE_WAY = 5, "5-Way"
        SIX_WAY = 6, "6-Way"
        EIGHT_WAY = 8, "8-Way"
    product_brand = models.CharField(
        max_length=30, 
        choices=ExtensionBrand.choices, 
        default=ExtensionBrand.GENERIC
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.EX
    )
    cable_length = models.FloatField(help_text="Length in meters (e.g., 1.5, 3.0, 5.0)")
    socket_count = models.IntegerField(choices=Sockets.choices, default=Sockets.FOUR_WAY)
    
    
class Battery(Product):
    class BatteryBrand(models.TextChoices):
        DURACELL = "duracell", "Duracell"
        ENERGIZER = "energizer", "Energizer"
        PANASONIC = "panasonic", "Panasonic"
        EVEREADY = "eveready", "Eveready"
        TIGER = "tiger", "Tiger"
        GENERIC = "generic", "Generic"

    class BatterySize(models.TextChoices):
        AA = "aa", "AA"
        AAA = "aaa", "AAA"
        C = "c", "C Size"
        D = "d", "D Size"
        NINE_V = "9v", "9V"
        CR2032 = "cr2032", "Button Cell (CR2032)"

    class Chemistry(models.TextChoices):
        ALKALINE = "alkaline", "Alkaline"
        ZINC_CARBON = "zinc_carbon", "Zinc Carbon (Heavy Duty)"
        LITHIUM = "lithium", "Lithium"
        NIMH = "nimh", "NiMH (Rechargeable)"

    size = models.CharField(max_length=10, choices=BatterySize.choices, default=BatterySize.AA)
    chemistry = models.CharField(max_length=20, choices=Chemistry.choices, default=Chemistry.ALKALINE)
    pack_count = models.PositiveSmallIntegerField(default=1, help_text="Number of batteries in the pack")

    product_brand = models.CharField(
        max_length=30, 
        choices=BatteryBrand.choices, 
        default=BatteryBrand.GENERIC
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.BT
    )
    
    
# Electric testers
class ElectricTester(Product):
    class ElectricTesterBrand(models.TextChoices):
        INGCO = "ingco", "Ingco"
        TOLSEN = "tolsen", "Tolsen"
        STANLEY = "stanley", "Stanley"
        GENERIC = "generic", "Generic"
        OTHER = "other", "Other"

    class TesterType(models.TextChoices):
        NEON = "neon", "Neon Contact (Classic)"
        DIGITAL = "digital", "Digital Display"
        NON_CONTACT = "non_contact", "Non-Contact (Voltage Detector)"
        
    product_brand = models.CharField(
        max_length=30, 
        choices=ElectricTesterBrand.choices, 
        default=ElectricTesterBrand.GENERIC
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.ELT
    )
    tester_type = models.CharField(
        max_length=20, 
        choices=TesterType.choices, 
        default=TesterType.NEON
    )
    voltage_range = models.CharField(
        max_length=30, 
        default="100V - 500V", 
        help_text="e.g., 12V-250V or 100V-500V"
    )

    
    
class SuperGlue(Product):
    class SuperGlueBrand(models.TextChoices):
        EVOSTICK = "evostick", "Evostick"
        ROCKET = "rocket", "Rocket"
        PATTEX = "pattex", "Pattex"
        GENERIC = "generic", "Generic"
        OTHER = "other", "Other"
        
    product_brand = models.CharField(
        max_length=30, 
        choices=SuperGlueBrand.choices, 
        default=SuperGlueBrand.EVOSTICK
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.SPG
    )
    
    
    
class Bulb(Product):
    class BulbBrand(models.TextChoices):
        PHILIPS = "philips", "Philips"
        OSRAM = "osram", "Osram"
        OPPLE = "opple", "Opple"
        GE = "ge", "General Electric"
        GENERIC = "generic", "Generic"

    class BulbTech(models.TextChoices):
        LED = "led", "LED"
        INCANDESCENT = "incandescent", "Incandescent"
        CFL = "cfl", "Fluorescent (CFL)"
        HALOGEN = "halogen", "Halogen"

    class LightColor(models.TextChoices):
        WARM_WHITE = "warm_white", "Warm White (Yellow)"
        DAYLIGHT = "daylight", "Daylight (White)"
        COOL_WHITE = "cool_white", "Cool White"
        
    product_brand = models.CharField(
        max_length=30, 
        choices=BulbBrand.choices, 
        default=BulbBrand.GENERIC
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.BLB
    )
    bulb_technology = models.CharField(max_length=20, choices=BulbTech.choices, default=BulbTech.LED)
    light_color = models.CharField(max_length=20, choices=LightColor.choices, default=LightColor.DAYLIGHT)
    wattage = models.IntegerField(help_text="Wattage (e.g., 9, 12, 15)")
    
    
class WallSocket(Product):
    class WallSocketBrand(models.TextChoices):
        ORANGE = "orange", "Orange"
        TRIONIC = "trionic", "Trionic"
        CHINT = "chint", "Chint"
        SCHNEIDER = "schneider", "Schneider"
        ABB = "abb", "ABB"
        GENERIC = "generic", "Generic"

    class SocketGang(models.IntegerChoices):
        SINGLE = 1, "Single (1-Gang)"
        DOUBLE = 2, "Double (2-Gang)"

    gangs = models.IntegerField(choices=SocketGang.choices, default=SocketGang.SINGLE)
    has_usb = models.BooleanField(default=False, verbose_name="Has USB Ports")
    has_type_c_connection=models.BooleanField(default=False,verbose_name="Has Type-C Connection")
    product_brand = models.CharField(
        max_length=30, 
        choices=WallSocketBrand.choices, 
        default=WallSocketBrand.ORANGE
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.WS.label
    )
    
    

class FridgeTvGuard(Product):
    class GuardBrand(models.TextChoices):
        SOLLATEK = "sollatek", "Sollatek"
        TAG_GUARD = "tag_guard", "Tag Guard"
        DIGITAL_SENTRY = "digital_sentry", "Digital Sentry"
        OPPLE = "opple", "Opple"
        GENERIC = "generic", "Generic"

    class GuardType(models.TextChoices):
        FRIDGE = "fridge", "Fridge Guard (High Power/Long Delay)"
        TV = "tv", "TV Guard (Low Power/Short Delay)"
        A_V = "av", "AVS (General Audio/Visual)"

    guard_type = models.CharField(
        max_length=15, 
        choices=GuardType.choices, 
        default=GuardType.FRIDGE
    )
    
    amps = models.IntegerField(default=13, help_text="Amperage (e.g., 5, 13, 15)")
    wait_time = models.SmallIntegerField(
        default=3, 
        help_text="Delay time before reconnecting power"
    )

    product_brand = models.CharField(
        max_length=30, 
        choices=GuardBrand.choices, 
        default=GuardBrand.SOLLATEK
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.FTG
    )


class TVRemoteBrands(models.TextChoices):
    VITRON = "vitron", "Vitron"
    SAMSUNG = "samsung", "Samsung"
    LG = "lg", "LG"
    SONY = "sony", "Sony"
    PANASONIC = "panasonic", "Panasonic"
    TOSHIBA = "toshiba", "Toshiba"
    HISENSE = "hisense", "Hisense"
    TCL = "tcl", "TCL"
    PHILIPS = "philips", "Philips"
    SHARP = "sharp", "Sharp"
    VIZIO = "vizio", "Vizio"
    MI = "mi", "Xiaomi / Mi"
    ONEPLUS = "oneplus", "OnePlus"
    HAIER = "haier", "Haier"
    SKYWORTH = "skyworth", "Skyworth"
    INSIGNIA = "insignia", "Insignia"
    HITACHI = "hitachi", "Hitachi"
    SANYO = "sanyo", "Sanyo"
    GRUNDIG = "grundig", "Grundig"
    JVC = "jvc", "JVC"
    PIONEER = "pioneer", "Pioneer"
    RCA = "rca", "RCA"
    WESTINGHOUSE = "westinghouse", "Westinghouse"
    ELEMENT = "element", "Element"
    KONKA = "konka", "Konka"
    POLAROID = "polaroid", "Polaroid"
    MAGNAVOX = "magnavox", "Magnavox"
    SEIKI = "seiki", "Seiki"
    
    GENERIC = "generic", "Generic"
    UNIVERSAL = "universal", "Universal (Multi-brand)"

class TvRemote(Product):
    class RemoteType(models.TextChoices):
        SMART = "smart", "Smart Remote (with Netflix/YouTube buttons)"
        STANDARD = "standard", "Standard IR Remote"
        UNIVERSAL = "universal", "Universal / Replacement"

    remote_type = models.CharField(
        max_length=20, 
        choices=RemoteType.choices, 
        default=RemoteType.STANDARD
    )
    is_programmable = models.BooleanField(
        default=False, 
        help_text="Can it be programmed for different TV models?"
    )

    product_brand = models.CharField(
        max_length=30, 
        choices=TVRemoteBrands.choices,
        default=TVRemoteBrands.VITRON
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.TR
    )
    
    
class BulbHolder(Product):
    class BulbHolderBrand(models.TextChoices):
        PANDA = "panda", "Panda"
        METRO = "metro", "Metro"
        TRIONIC = "trionic", "Trionic"
        CHINT = "chint", "Chint"
        ORANGE = "orange", "Orange"
        GENERIC = "generic", "Generic"

    class HolderType(models.TextChoices):
        BATON = "baton", "Baton (Fixed to Wall/Ceiling)"
        PENDANT = "pendant", "Pendant (Hanging)"
        ADAPTOR = "adaptor", "Adaptor (e.g. Pin to Screw)"
        ANGLED = "angled", "Angled Holder"

    class ConnectionType(models.TextChoices):
        BC = "bc", "B22 (Pin Type)"
        ES = "es", "E27 (Screw Type)"

    holder_type = models.CharField(
        max_length=20, 
        choices=HolderType.choices, 
        default=HolderType.BATON
    )
    connection_type = models.CharField(
        max_length=10, 
        choices=ConnectionType.choices, 
        default=ConnectionType.BC
    )

    product_brand = models.CharField(
        max_length=30, 
        choices=BulbHolderBrand.choices, 
        default=BulbHolderBrand.GENERIC
    )
    product_category = models.CharField(
        max_length=30, 
        default=ProductCategory.BH
    )
    
    
class ShaverBrand(models.TextChoices):
    # Professional & Barbershop Standards
    WAHL = "WAHL", _("Wahl")  # The gold standard in African kinyozis
    ANDIS = "ANDIS", _("Andis")
    BABYLISS = "BABYLISS", _("BaBylissPRO")
    MOSER = "MOSER", _("Moser")
    
    # Popular Home & Budget Brands (Very high presence in Kenya)
    GEEMY = "GEEMY", _("Geemy")
    KEMEI = "KEMEI", _("Kemei")
    ORAIMO = "ORAIMO", _("Oraimo")  # Growing rapidly via the 'SmartClipper' series
    DINGLING = "DINGLING", _("Dingling")
    VGR = "VGR", _("VGR")
    
    # Established Consumer Brands
    PHILIPS = "PHILIPS", _("Philips")
    BRAUN = "BRAUN", _("Braun")
    PANASONIC = "PANASONIC", _("Panasonic")
    XIAOMI = "XIAOMI", _("Xiaomi / Enchen")
    
    # Grooming & Lifestyle
    MANSCAPED = "MANSCAPED", _("Manscaped")
    BEVEL = "BEVEL", _("Bevel")
    
    
class ShavingMachine(Product):
    product_brand=models.CharField(max_length=20,choices=ShaverBrand.choices,default=ShaverBrand.ORAIMO)
    product_category=models.CharField(max_length=20,default=ProductCategory.SHM,editable=False)
    
class WaterHeaterType(models.TextChoices):
    IMMERSION_COIL = "COIL", _("Immersion Rod/Coil")
    KETTLE = "KETTLE", _("Electric Jug/Kettle")

class HeaterBrand(models.TextChoices):
    # Brands with huge presence in East Africa/Kenya
    SAYONA = "SAYONA", _("Sayona")
    RAMTONS = "RAMTONS", _("Ramtons")  # Very popular in Kenya
    VON = "VON", _("Von (Hotpoint)")
    NUNIX = "NUNIX", _("Nunix")
    MICA = "MICA", _("Mica")
    
    # Common "Coil" brands often seen in local shops
    RHINO = "RHINO", _("Rhino")
    LONTOR = "LONTOR", _("Lontor")
    
    # Premium/Global
    PHILIPS = "PHILIPS", _("Philips")
    KENWOOD = "KENWOOD", _("Kenwood")
    BLACK_DECKER = "BLACK_DECKER", _("Black & Decker")

class WaterHeater(Product):
    product_brand=models.CharField(max_length=20,choices=HeaterBrand.choices,default=HeaterBrand.SAYONA)
    product_category=models.CharField(max_length=20,default=ProductCategory.WH,editable=False)
    heater_type=models.CharField(max_length=30,choices=WaterHeaterType.choices,default=WaterHeaterType.IMMERSION_COIL)
    wattage = models.IntegerField(help_text="Power in Watts (e.g., 2000)")
    
    
    
class GasBurnerType(models.TextChoices):
    CYLINDER_TOP = "CYLINDER_TOP", _("Cylinder-top")
    TABLE_TOP = "TABLE_TOP", _("Table-top Cooker")

class GasBurnerBrand(models.TextChoices):
    # Brands dominant for Table-tops
    MIKA = "MIKA", _("Mika")
    RAMTONS = "RAMTONS", _("Ramtons")
    VON = "VON", _("Von (Hotpoint)")
    NUNIX = "NUNIX", _("Nunix")
    AILYONS = "AILYONS", _("Ailyons")
    SAYONA = "SAYONA", _("Sayona")
    
    # Brands dominant for Cylinder-top (Meko) Burners
    TOTALENERGIES = "TOTAL", _("TotalEnergies")
    RUBIS = "RUBIS", _("Rubis / K-Gas")
    PROGAS = "PROGAS", _("Progas")
    AFRIGAS = "AFRIGAS", _("Afrigas")
    RASHNIK = "RASHNIK", _("Rashnik")
    # Generic highly-rated hardware brands
    HR = "HR", _("HR Strong")
    
    
class GasBurner(Product):
    product_category=models.CharField(max_length=30,default=ProductCategory.GB,editable=False)
    product_brand=models.CharField(max_length=20,choices=GasBurnerBrand.choices,default=GasBurnerBrand.TOTALENERGIES)
    burner_type=models.CharField(max_length=20,choices=GasBurnerType.choices,default=GasBurnerType.CYLINDER_TOP)
    burner_count=models.SmallIntegerField(default=0)
    

    
class SmartWatchCharger(PhoneAccessories):
    class SmartwatchConnector(models.TextChoices):
        # Common universal magnetic pins found in local shops
        MAGNETIC_2PIN_2_84 = "MAG2_284", _("2-Pin Magnetic (2.84mm)")
        MAGNETIC_2PIN_4_0 = "MAG2_40", _("2-Pin Magnetic (4.0mm)")
        MAGNETIC_4PIN_7_62 = "MAG4_762", _("4-Pin Magnetic (7.62mm)")
        
        # Brand-specific wireless/cradles
        WIRELESS_PUCK = "WIRELESS", _("Wireless Magnetic Puck (Apple/Samsung)")
        GARMIN_PLUG = "GARMIN", _("Garmin 4-Pin Plug")
        FITBIT_CLIP = "FITBIT", _("Fitbit Clamp/Clip")
    product_brand=models.CharField(max_length=20,choices=SmartwatchBrand.choices,default=SmartwatchBrand.ORAIMO)
    product_category=models.CharField(max_length=30,default=ProductCategory.SWC,editable=False)
    connector_type = models.CharField(
        max_length=15,
        choices=SmartwatchConnector.choices,
        default=SmartwatchConnector.MAGNETIC_2PIN_4_0,
        help_text="The physical pin connection style"
    )
    
    
# Dongles
# WIFI DONGLE 
class WifiBrand(models.TextChoices):
    TPLINK = "TP-LINK", _("TP-Link")
    NETGEAR = "NETGEAR", _("Netgear")
    ASUS = "ASUS", _("Asus")
    DLINK = "D-LINK", _("D-Link")
    TENDA = "TENDA", _("Tenda")
    MERCUSYS = "MERCUSYS", _("Mercusys")
    BROSTREND = "BROSTREND", _("BrosTrend")
    EDUP = "EDUP", _("EDUP")
    ALFA = "ALFA", _("Alfa Network")
    GENERIC = "GENERIC", _("Generic")
    OTHER="OTHER",_("Other")

class WifiProtocol(models.TextChoices):
    WIFI_4 = "N", _("Wi-Fi 4 (802.11n)")
    WIFI_5 = "AC", _("Wi-Fi 5 (802.11ac)")
    WIFI_6 = "AX", _("Wi-Fi 6 (802.11ax)")
    WIFI_6E = "AXE", _("Wi-Fi 6E (6GHz)")
    WIFI_7 = "BE", _("Wi-Fi 7 (802.11be)")

class WifiDongle(Product):
    product_brand = models.CharField(max_length=20, choices=WifiBrand.choices,default=WifiBrand.DLINK)
    product_category=models.CharField(max_length=20,default=ProductCategory.WFD,editable=False)
    protocol = models.CharField(max_length=5, choices=WifiProtocol.choices,default=WifiProtocol.WIFI_6)
    max_speed_mbps = models.PositiveIntegerField(help_text="e.g., 1200",verbose_name="Max Speed in Mbs")
    is_dual_band = models.BooleanField(default=False)
    has_antenna = models.BooleanField(default=False)
    
    
# BLUETOOTH DONGLE
class BluetoothBrand(models.TextChoices):
    UGREEN = "UGREEN", _("UGreen")
    TPLINK = "TP-LINK", _("TP-Link")
    ASUS = "ASUS", _("Asus")
    LOGITECH = "LOGITECH", _("Logitech")
    AVANTREE = "AVANTREE", _("Avantree")
    ZEXMTE = "ZEXMTE", _("Zexmte")
    SENA = "SENA", _("Sena")
    PLUGGABLE = "PLUGGABLE", _("Pluggable")
    TECHKEY = "TECHKEY", _("Techkey")
    GENERIC = "GENERIC", _("Generic")
    OTHER="OTHER",_("Other")

class BluetoothVersion(models.TextChoices):
    V4_0 = "4.0", _("Bluetooth 4.0")
    V5_0 = "5.0", _("Bluetooth 5.0")
    V5_3 = "5.3", _("Bluetooth 5.3")
    V5_4 = "5.4", _("Bluetooth 5.4")

class BluetoothDongle(Product):
    product_category=models.CharField(max_length=20,default=ProductCategory.BLD,editable=False)
    product_brand=models.CharField(max_length=20,choices=BluetoothBrand.choices,default=BluetoothBrand.TPLINK)
    version = models.CharField(max_length=5, choices=BluetoothVersion.choices,default=BluetoothVersion.V5_0)
    plug_type = models.CharField(max_length=10, default="USB-A", choices=[
        ("USB-A", "USB Type-A"),
        ("USB-C", "USB Type-C")
    ])


# BLUETOOTH SPEAKER

class BluetoothSpeakerBrand(models.TextChoices):
    # Global Leaders
    JBL = "JBL", _("JBL")
    SONY = "SONY", _("Sony")
    BOSE = "BOSE", _("Bose")
    MARSHALL = "MARSHALL", _("Marshall")
    ULTIMATE_EARS = "UE", _("Ultimate Ears")
    ORAIMO="ORAIMO",_("Oraimo")
    
    # High-Value / Consumer Favorites
    ANKER_SOUNDCORE = "ANKER", _("Anker Soundcore")
    SONOS = "SONOS", _("Sonos")
    BEATS = "BEATS", _("Beats by Dre")
    TRIBIT = "TRIBIT", _("Tribit")
    EDIFIER = "EDIFIER", _("Edifier")
    
    # Smart & Home Focused
    GOOGLE = "GOOGLE", _("Google Nest")
    APPLE = "APPLE", _("Apple HomePod")
    XIAOMI = "XIAOMI", _("Xiaomi")
    GENERIC = "GENERIC", _("Generic / Unbranded")

class SpeakerSize(models.TextChoices):
    POCKET = "POCKET", _("Pocket (e.g., JBL Go)")
    PORTABLE = "PORTABLE", _("Portable (e.g., JBL Flip/Charge)")
    BOOMBOX = "BOOMBOX", _("Boombox (e.g., Sony ULT Field 7)")
    PARTY = "PARTY", _("Party Speaker (Mains Powered)")

class BluetoothSpeaker(Product):
    product_brand = models.CharField(max_length=20, choices=BluetoothSpeakerBrand.choices,default=BluetoothSpeakerBrand.ORAIMO)
    product_category=models.CharField(max_length=20,default=ProductCategory.BTS,editable=False)
    size_category = models.CharField(max_length=15, choices=SpeakerSize.choices,default=SpeakerSize.PORTABLE)
    # Core Specs for 2026
    bluetooth_version = models.CharField(max_length=5, default="5.3")
    wattage = models.PositiveIntegerField(help_text="Output power in Watts")
    battery_life_hours = models.PositiveIntegerField()
    
    # Features
    has_rgb_lights = models.BooleanField(default=False)
    can_power_bank = models.BooleanField(default=False, help_text="Can charge other devices")
    
    
    
class TVBoxBrand(models.TextChoices):
    # Officially Certified (Top Tier in Kenya/Africa)
    XIAOMI = "XIAOMI", _("Xiaomi (Mi Box/Stick)")
    GOOGLE = "GOOGLE", _("Google (Chromecast/Streamer)")
    AMAZON = "AMAZON", _("Amazon (Fire TV Stick)")
    SKYWORTH = "SKYWORTH", _("Skyworth / Leap-S3")
    APPLE = "APPLE", _("Apple TV")
    EMATIC = "EMATIC", _("Ematic")
    NVIDIA = "NVIDIA", _("Nvidia Shield")
    
    # Popular Budget/Open-Box Brands
    MXQ = "MXQ", _("MXQ Pro")
    X96 = "X96", _("X96 Mini/Max")
    H96 = "H96", _("H96 Max")
    TRANSPEED = "TRANSPEED", _("Transpeed")
    GENERIC = "GENERIC", _("Generic Android Box")

class TVBoxResolution(models.TextChoices):
    HD = "HD", _("HD (1080p)")
    UHD_4K = "4K", _("4K Ultra HD")
    UHD_8K = "8K", _("8K Ultra HD")

class TvBox(Product):
    product_brand=models.CharField(max_length=20,default=TVBoxBrand.XIAOMI,choices=TVBoxBrand.choices)
    product_category=models.CharField(max_length=20,default=ProductCategory.TVB,editable=False)
    
    # Technical Specs
    os_version = models.CharField(max_length=50, help_text="e.g., Android TV 11, FireOS")
    ram_gb = models.PositiveSmallIntegerField(default=2,verbose_name="RAM (GB)")
    storage_gb = models.PositiveSmallIntegerField(default=8,verbose_name="ROM (GB)")
    max_resolution = models.CharField(
        max_length=5, 
        choices=TVBoxResolution.choices, 
        default=TVBoxResolution.UHD_4K
    )
    
    # Connectivity
    has_ethernet_port = models.BooleanField(default=False)
    has_usb_ports = models.BooleanField(default=True)
    supports_5ghz_wifi = models.BooleanField(default=True)
    
    # Certification (Crucial for Netflix/Disney+)
    is_google_certified = models.BooleanField(default=False)
    is_netflix_certified = models.BooleanField(default=False)
    

# TV Aerial
class AerialType(models.TextChoices):
    INDOOR = "INDOOR", _("Indoor (Flat/Rabbit Ears)")
    OUTDOOR = "OUTDOOR", _("Outdoor (Yagi/Grid)")
    SATELLITE = "DISH", _("Satellite Dish")

class AerialBrand(models.TextChoices):
    # Dominant for Digital/DVB-T2 in Kenya & Africa
    GOTV = "GOTV", _("GOtv Official Aerial")
    PHILLISTAR = "PHILLISTAR", _("Phillistar")
    SONAR = "SONAR", _("Sonar")
    SKYWORTH = "SKYWORTH", _("Skyworth")
    AERIAL_KING = "AERIAL_KING", _("Aerial King")
    
    # Generic / High-Gain specialized
    RASHNIK = "RASHNIK", _("Rashnik")
    GENERIC = "GENERIC", _("Generic High-Gain")
    # Satellite Brands (often listed as aerials in retail)
    DSTV = "DSTV", _("DStv (MultiChoice)")

class TvAerial(Product):
    product_brand=models.CharField(max_length=20,choices=AerialBrand.choices,default=AerialBrand.GOTV)
    product_category=models.CharField(max_length=20,default=ProductCategory.TVA,editable=False)
    aerial_type = models.CharField(
        max_length=20, 
        choices=AerialType.choices, 
        default=AerialType.OUTDOOR
    )
    
    includes_cable = models.BooleanField(default=True)
    has_booster = models.BooleanField(
        default=False, 
        help_text="Built-in signal amplifier/booster"
    )
    
# PHONE BATTERY
class BatteryInstallation(models.TextChoices):
    REMOVABLE = "REMOVABLE", _("Removable (User-replaceable)")
    INTERNAL = "INTERNAL", _("Internal (Requires Installation)")

class BatteryBrand(models.TextChoices):
    # OEM Brands (The phone manufacturers)
    SAMSUNG = "SAMSUNG", _("Samsung")
    APPLE = "APPLE", _("Apple")
    NOKIA = "NOKIA", _("Nokia")
    TECNO = "TECNO", _("Tecno")
    INFINIX = "INFINIX", _("Infinix")
    ITEL = "ITEL", _("Itel")
    OPPO = "OPPO", _("Oppo")
    XIAOMI = "XIAOMI", _("Xiaomi")
    HUAWEI = "HUAWEI", _("Huawei")
    
    # Aftermarket/Replacement Specialists
    ORAIMO = "ORAIMO", _("Oraimo")
    AMAYA = "AMAYA", _("Amaya")
    ANKER = "ANKER", _("Anker")
    MTECH = "MTECH", _("M-Tech")
    GENERIC = "GENERIC", _("Generic / Other")

class PhoneBattery(Product):
    product_brand=models.CharField(max_length=20,choices=BatteryBrand.choices,default=BatteryBrand.AMAYA)
    product_category=models.CharField(max_length=20,default=ProductCategory.PBR,editable=False)
    
    # This captures BL-5C for feature phones or EB-BN970ABU for smartphones
    battery_code = models.CharField(
        max_length=30, 
        help_text=_("e.g., BL-5C, EB-BG991ABY, A2111")
    )
    
    installation_type = models.CharField(
        max_length=15,
        choices=BatteryInstallation.choices,
        default=BatteryInstallation.INTERNAL
    )
    capacity_mah = models.PositiveIntegerField(help_text=_("Capacity in mAh"))



class VideoCableBrand(models.TextChoices):
    # Prominent brands in African and International markets
    VENTION = "VENTION", _("Vention")
    UGREEN = "UGREEN", _("UGreen")
    TRONIC = "TRONIC", _("Tronic")
    SONAR = "SONAR", _("Sonar")
    LOGILINK = "LOGILINK", _("LogiLink")
    AMAZON_BASICS = "AMAZON", _("Amazon Basics")
    GENERIC = "GENERIC", _("Generic / Unbranded")

class CableInterface(models.TextChoices):
    HDMI = "HDMI", _("HDMI")
    VGA = "VGA", _("VGA")
    HDMI_TO_VGA = "HDMI_VGA", _("HDMI to VGA (Adapter Cable)")

class VideoCable(Product):
    product_brand=models.CharField(max_length=20,choices=VideoCableBrand.choices,default=VideoCableBrand.LOGILINK)
    product_category=models.CharField(max_length=20,default=ProductCategory.VC,editable=False)
    interface_type = models.CharField(max_length=10, choices=CableInterface.choices,default=CableInterface.HDMI)
    
    # Length is the most common customer filter
    length_meters = models.FloatField(help_text=_("Length in meters (e.g., 1.5, 3.0, 10)"))
    is_braided = models.BooleanField(default=False, verbose_name=_("Nylon Braided"))
    has_gold_connectors = models.BooleanField(default=True)
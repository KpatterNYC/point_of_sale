from django import forms

from dn_products import models
RESTOCK_THRESHOLD_HT="Triggers an alert when the stock drops below the set value."


SELECT={"class":"select select-sm w-full"}
INPUT={"class":"input input-sm w-full"}
CHECKBOX={"class":"checkbox checkbox-primary"}


class BaseForm(forms.ModelForm):
    class Meta:
        exclude=("pictures",'product_attributes',"stocker","added_date","product_category")
        help_texts={
            "restock_threshold":RESTOCK_THRESHOLD_HT,
        }
        widgets={
            'product_name': forms.TextInput(attrs=INPUT),
            'product_category': forms.TextInput(attrs=INPUT),
            'product_brand': forms.Select(attrs=SELECT),
            'product_buy_price': forms.NumberInput(attrs=INPUT),
            'product_sell_price': forms.NumberInput(attrs=INPUT),
            'product_count': forms.NumberInput(attrs=INPUT),
            'restock_threshold': forms.NumberInput(attrs=INPUT),
            'added_date': forms.DateTimeInput(attrs=INPUT),
            'product_discount':forms.NumberInput(attrs=INPUT)
        }
        
    
    def clean_product_name(self):
        product_name:str=self.cleaned_data.get("product_name")
        return product_name.strip().title() if product_name  else product_name
        
        

# FACTORY 
class Phones(forms.ModelForm):
    class Meta(BaseForm.Meta):
        widgets={
            **BaseForm.Meta.widgets,
            'screen_size':forms.TextInput(attrs=INPUT),
            'ram':forms.TextInput(attrs=INPUT),
            'rom':forms.TextInput(attrs=INPUT),
            'charger_type':forms.Select(attrs=SELECT),
            "battery_capacity":forms.TextInput(attrs=INPUT),
            'sim_type':forms.Select(attrs=SELECT),
        }


class Electronics:
    class Meta(BaseForm.Meta):
        widgets={
            **BaseForm.Meta.widgets,
            'serial_no': forms.TextInput(attrs=INPUT),
            'model_no': forms.TextInput(attrs=INPUT),
            'bluetooth': forms.CheckboxInput(attrs=CHECKBOX),
        }
        
# Phones (Smart/FeaturedPhones)

class SmartPhoneForm(forms.ModelForm):
    class Meta(Phones.Meta):
        model=models.SmartPhone
        help_texts={
            "restock_threshold":RESTOCK_THRESHOLD_HT,
        }

class FeaturedPhoneForm(forms.ModelForm):
    class Meta(Phones.Meta):
        model=models.FeaturedPhone
        help_texts={
            "restock_threshold":RESTOCK_THRESHOLD_HT,
        }

# Phone Accessoreis
class PowerBankForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.PowerBank
        widgets = {
                    **BaseForm.Meta.widgets,
                   'capacity': forms.NumberInput(attrs=INPUT),
                   'product_subcategory': forms.TextInput(attrs=INPUT)
                   }

class PhoneChargerForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.PhoneCharger
        widgets = {
                    **BaseForm.Meta.widgets,
                   'charger_type': forms.Select(attrs=SELECT),
                   'charging_port': forms.Select(attrs=SELECT),
                   'product_subcategory': forms.TextInput(attrs=INPUT)
                   }


class DataCableForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.DataCable
        widgets = {
                **BaseForm.Meta.widgets,
                   'cable_type': forms.Select(attrs=SELECT),
                   'product_subcategory': forms.TextInput(attrs=INPUT),
                   'length':forms.NumberInput(attrs=INPUT)
                   }
        help_texts={
            **BaseForm.Meta.help_texts,
            'length':'in (Meters)',
        }

class HeadphonesAndEarphonesForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.HeadphonesAndEarphones
        widgets = {
                    **BaseForm.Meta.widgets,
                   'e_type': forms.Select(attrs=SELECT),
                   'bluetooth': forms.CheckboxInput(attrs=CHECKBOX),
                   'wired': forms.CheckboxInput(attrs=CHECKBOX),
                   'c_type': forms.Select(attrs=SELECT)}


class ScreenProtectorForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.ScreenProtector
        exclude=BaseForm.Meta.exclude + ("compatible_phones",)
        widgets = {
                    **BaseForm.Meta.widgets,
                   "phone_brand":forms.Select(attrs=SELECT),
                   'compatible_phones': forms.TextInput(attrs=INPUT),
                   'product_subcategory': forms.TextInput(attrs=INPUT)
                   }

class PhoneCasingForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.PhoneCasing
        widgets = {
                **BaseForm.Meta.widgets,
                'product_subcategory': forms.TextInput(attrs=INPUT),
                'phone_brand':forms.Select(attrs=SELECT),
                'phone_model':forms.TextInput(attrs=INPUT),
        }
        
                    

class MusicSystemForm(forms.ModelForm):
    class Meta(Electronics.Meta):
        model = models.MusicSystem
        widgets = {
                    **Electronics.Meta.widgets,
                   'channel': forms.NumberInput(attrs=INPUT),
                   'watts': forms.NumberInput(attrs=INPUT),
                   'system_type': forms.Select(attrs=SELECT),
                   }

class FlatScreenTvForm(forms.ModelForm):
    class Meta(Electronics.Meta):
        model = models.FlatScreenTv
        widgets = {**Electronics.Meta.widgets,
                   'inches': forms.NumberInput(attrs=INPUT),
                   'resolution': forms.Select(attrs=SELECT),
                   'frameless': forms.CheckboxInput(attrs=CHECKBOX),
                   'tv_type': forms.Select(attrs=SELECT)}
        
class SmartWatchForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model = models.SmartWatch
        widgets={
            **BaseForm.Meta.widgets,
            "amoled_screen":forms.CheckboxInput(attrs=CHECKBOX),
            "form_factor":forms.Select(attrs=SELECT),
            "is_rugged":forms.CheckboxInput(attrs=CHECKBOX),
            "compatibility":forms.Select(attrs=SELECT)
        }

# STORAGE
class StorageForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        widgets={
            **BaseForm.Meta.widgets,
            "product_category":forms.TextInput(attrs=INPUT),
            "product_brand":forms.Select(attrs=SELECT),
            "size":forms.NumberInput(attrs=INPUT),
        }
class MemoryCardForm(StorageForm):
    class Meta(StorageForm.Meta):
        model=models.MemoryCard
class FlashDiskForm(StorageForm):
    class Meta(StorageForm.Meta):
        model=models.FlashDisk
class HardDiskForm(StorageForm):
    class Meta(StorageForm.Meta):
        model=models.HardDisk
class SsDiskForm(StorageForm):
    class Meta(StorageForm.Meta):
        model=models.SsDisk

# ROUTER
class RouterForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.Router
        widgets={
            **BaseForm.Meta.widgets,
            "wifi_standard":forms.Select(attrs=SELECT),
            "total_speed_mbps":forms.NumberInput(attrs=INPUT),
            "lan_ports_count":forms.NumberInput(attrs=INPUT),
            "has_mesh_support":forms.CheckboxInput(attrs=CHECKBOX)
        }
        
# COMPUTER MOUSE
class ComputerMouseForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.ComputerMouse
        widgets={
            **BaseForm.Meta.widgets,
            "connection":forms.Select(attrs=SELECT),
            "max_dpi":forms.NumberInput(attrs=INPUT),
            "is_programmable":forms.CheckboxInput(attrs=CHECKBOX)
        }
        

class ComputerKeyboardForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.ComputerKeyboard
        widgets={
            **BaseForm.Meta.widgets,
            "size":forms.Select(attrs=SELECT),
            "is_hotswappable":forms.CheckboxInput(attrs=CHECKBOX),
            "has_rgb":forms.CheckboxInput(attrs=CHECKBOX),
            "connection":forms.Select(attrs=SELECT)
        }
        
        
# Hot Shower

class HotShowerForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.HotShower
        widgets={
            **BaseForm.Meta.widgets,
            "control":forms.Select(attrs=SELECT),
            "wattage":forms.NumberInput(attrs=INPUT)
        }
        
# Extension
class ExtensionForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.Extension
        widgets={
            **BaseForm.Meta.widgets,
            "cable_length":forms.NumberInput(attrs=INPUT),
            "socket_count":forms.Select(attrs=SELECT)
        }
        
class BatteryForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.Battery
        widgets={
            **BaseForm.Meta.widgets,
            "size":forms.Select(attrs=SELECT),
            "chemistry":forms.Select(attrs=SELECT),
            "pack_count":forms.NumberInput(attrs=INPUT)
        }
        
        
class ElectricTesterForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.ElectricTester
        widgets={
            **BaseForm.Meta.widgets,
            "tester_type":forms.Select(attrs=SELECT),
            "voltage_range":forms.TextInput(attrs=INPUT),
        }
        
class SuperGlueForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.SuperGlue
        widgets={
            **BaseForm.Meta.widgets,
        }
        
class BulbForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.Bulb
        widgets={
            **BaseForm.Meta.widgets,
            "bulb_technology":forms.Select(attrs=SELECT),
            "light_color":forms.Select(attrs=SELECT),
            "wattage":forms.NumberInput(attrs=INPUT)
        }
        
class WallSocketForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.WallSocket
        widgets={
            **BaseForm.Meta.widgets,
            "gangs":forms.Select(attrs=SELECT),
            "has_usb":forms.CheckboxInput(attrs=CHECKBOX),
            "has_type_c_connection":forms.CheckboxInput(attrs=CHECKBOX)
        }
 
 
 
class FridgeTvGuardForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.FridgeTvGuard
        widgets={
            **BaseForm.Meta.widgets,
            "guard_type":forms.Select(attrs=SELECT),
            "amps":forms.NumberInput(attrs=INPUT),
            "wait_time":forms.NumberInput(attrs=INPUT),
        }
        

class TvRemoteForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.TvRemote
        widgets={
            **BaseForm.Meta.widgets,
            "remote_type":forms.Select(attrs=SELECT),
            "is_programmable":forms.CheckboxInput(attrs=CHECKBOX)
        }
        
class BulbHolderForm(forms.ModelForm):
    class Meta(BaseForm.Meta):
        model=models.BulbHolder
        widgets={
            **BaseForm.Meta.widgets,
            "holder_type":forms.Select(attrs=SELECT),
            "connection_type":forms.Select(attrs=SELECT)
        }
        
class ShavingMachineForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.ShavingMachine
        widgets={
            **BaseForm.Meta.widgets
        }
        

class WaterHeaterForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.WaterHeater
        widgets={
            **BaseForm.Meta.widgets,
            "heater_type":forms.Select(attrs=SELECT),
            "wattage":forms.TextInput(attrs=INPUT)
        }
        

class GasBurnerForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.GasBurner
        widgets={
            **BaseForm.Meta.widgets,
            "burner_count":forms.NumberInput(attrs=INPUT),
            "burner_type":forms.Select(attrs=SELECT)
        }
        
        
class SmartWatchChargerForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.SmartWatchCharger
        widgets={
            **BaseForm.Meta.widgets,
            "connector_type":forms.Select(attrs=SELECT)
        }
        
        
        

class WifiDongleForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.WifiDongle
        widgets={
            **BaseForm.Meta.widgets,
            "protocol":forms.Select(attrs=SELECT),
            "max_speed_mbps":forms.TextInput(attrs=INPUT),
            "is_dual_band":forms.CheckboxInput(attrs=CHECKBOX),
            "has_antenna":forms.CheckboxInput(attrs=CHECKBOX)
        }
        

class BluetoothDongleForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.BluetoothDongle
        widgets={
            **BaseForm.Meta.widgets,
            "version":forms.Select(attrs=SELECT),
            "plug_type":forms.Select(attrs=SELECT)
        }
        
        
class BluetoothSpeakerForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.BluetoothSpeaker
        widgets={
            **BaseForm.Meta.widgets,
            "size_category":forms.Select(attrs=SELECT),
            "bluetooth_version":forms.TextInput(attrs=INPUT),
            "wattage":forms.NumberInput(attrs=INPUT),
            "battery_life_hours":forms.NumberInput(attrs=INPUT),
            "has_rgb_lights":forms.CheckboxInput(attrs=CHECKBOX),
            "can_power_bank":forms.CheckboxInput(attrs=CHECKBOX)
        }
        

class TvBoxForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.TvBox
        widgets={
            **BaseForm.Meta.widgets,
            "os_version":forms.TextInput(attrs=INPUT),
            "ram_gb":forms.NumberInput(attrs=INPUT),
            "storage_gb":forms.NumberInput(attrs=INPUT),
            "max_resolution":forms.Select(attrs=SELECT),
            "has_ethernet_port":forms.CheckboxInput(attrs=CHECKBOX),
            "has_usb_ports":forms.CheckboxInput(attrs=CHECKBOX),
            "supports_5ghz_wifi":forms.CheckboxInput(attrs=CHECKBOX),
            "is_google_certified":forms.CheckboxInput(attrs=CHECKBOX),
            "is_netflix_certified":forms.CheckboxInput(attrs=CHECKBOX),
        }
        

class TvAerialForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.TvAerial
        widgets={
            **BaseForm.Meta.widgets,
            "aerial_type":forms.Select(attrs=SELECT),
            "includes_cable":forms.CheckboxInput(attrs=CHECKBOX),
            "has_booster":forms.CheckboxInput(attrs=CHECKBOX)
            
        }
        

class PhoneBatteryForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=models.PhoneBattery
        widgets={
             **BaseForm.Meta.widgets,
             "battery_code":forms.TextInput(attrs=INPUT),
             "installation_type":forms.Select(attrs=SELECT),
             "capacity_mah":forms.NumberInput(attrs=INPUT)
        }
        
class VideoCableForm(BaseForm):
     class Meta(BaseForm.Meta):
        model=models.VideoCable
        widgets={
            **BaseForm.Meta.widgets,
            "interface_type": forms.Select(attrs=SELECT),
            "length_meters":forms.NumberInput(attrs=INPUT),
            "is_braided":forms.CheckboxInput(attrs=CHECKBOX),
            "has_gold_connectors":forms.CheckboxInput(attrs=CHECKBOX)
        }
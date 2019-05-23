from .models.utils import to_lower_camel_case

from enum import Enum


class IdentificationWidget:
    birth_date: str
    first_name: str
    inn: str
    last_name: str
    middle_name: str
    oms: str
    passport: str
    snils: str

    __doc__ = """birth_date 	Дата рождения пользователя (в формате “ГГГГ-ММ-ДД”)
first_name 	Имя пользователя
middle_name 	Отчество пользователя
last_name 	Фамилия пользователя
passport 	Серия и номер паспорта пользователя (только цифры)
inn 	ИНН пользователя
snils 	Номер СНИЛС пользователя
oms 	Номер полиса ОМС пользователя
"""

    def as_dict(self):
        return {
            to_lower_camel_case(k): getattr(self, k)
            for k in vars(self).keys()
            if k[0] != "_"
        }


class PaymentTypes(Enum):
    incoming = IN = "IN"
    outgoing = OUT = "OUT"
    qiwi_card = QIWI_CARD = "QIWI_CARD"
    all = ALL = "ALL"


class Provider(Enum):
    """
    99 - Перевод на QIWI Wallet

    1963 - Перевод на карту Visa (карты российских банков)
    21013 - Перевод на карту MasterCard (карты российских банков)
    Для карт, выпущенных банками стран Азербайджан, Армения, Белоруссия, Грузия, Казахстан, Киргизия, Молдавия,
    Таджикистан, Туркменистан, Украина, Узбекистан:
        1960 – Перевод на карту Visa
        21012 – Перевод на карту MasterCard

    31652 - Перевод на карту национальной платежной системы МИР
    466 - Тинькофф Банк
    464 - Альфа-Банк
    821 - Промсвязьбанк
    815 - Русский Стандарт
    Идентификаторы операторов мобильной связи
    Идентификаторы других провайдеров
    1717 - платеж по банковским реквизитам"""

    QIWI_WALLET = 99

    VISA_RU = 1963
    VISA_FOREIGN = 1960

    MASTERCARD_RU = 21013
    MASTERCARD_FOREIGN = 21012

    MIR_CARD = 31652

    TINKOFF = TINKOFF_BANK = 466
    ALPHA = ALFA = ALFA_BANK = ALPHA_BANK = 464
    PROSVYAZ_BANK = 821
    RUSSKIY_STANDART = 815

    CUSTOM = 1717


class _ChequeTypes:
    JPEG = "JPEG"
    PDF = "PDF"

    def __contains__(self, item):
        return item in [self.JPEG, self.PDF]


ChequeTypes = _ChequeTypes()

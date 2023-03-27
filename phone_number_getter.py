import re
from onlinesimru import NumbersService


class RentPhoneForSMS:
    """ Retrieves phone number via API from onlinesimru """

    service = NumbersService('')

    def get_phone_number(self) -> tuple:
        """ Returns new number and it's tzid """

        new_number = self.service.get('Yandex', country=77, number=True)
        return new_number['number'], new_number['tzid']

    def get_phone_code(self, tzid: int):
        """ Waits and returns code which has been sent to phone """

        code = self.service.wait_code(tzid, timeout=10)

        return re.sub(r'[0-9]]', '', code)

import hog_rfid as RFID




def test_is_payment_successful_approved():
    card_id = "1234567890"
    result = RFID.is_payment_successful(card_id)
    assert result == True  # Assert that the payment is successful for approved ID

def test_is_payment_successful_not_approved():
    card_id = "1111111111"
    result = RFID.is_payment_successful(card_id)
    assert result == False  # Assert that the payment is not successful for non-approved ID


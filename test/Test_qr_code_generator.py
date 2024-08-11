import pytest
import os
import random
from qr_code_generator import qr_generate, qr_generatepay

def test_qr_generate(monkeypatch):
    def mock_randint(a, b):
        return 42  # Fixed value for predictable output

    monkeypatch.setattr(random, 'randint', mock_randint)
    qr_generate()
    assert os.path.exists("qr-img.jpg")
    os.remove("qr-img.jpg")

def test_qr_generatepay(monkeypatch):
    def mock_randint(a, b):
        return 45  # Fixed value for predictable output

    monkeypatch.setattr(random, 'randint', mock_randint)
    qr_generatepay()
    assert os.path.exists("qr-pay.jpg")
    os.remove("qr-pay.jpg")

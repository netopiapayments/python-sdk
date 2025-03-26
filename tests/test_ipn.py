import unittest
import base64
import json
import hashlib
from datetime import datetime, timedelta
from types import SimpleNamespace

from jwt import encode

from netopia_sdk.config import Config
from netopia_sdk.client import PaymentClient
from netopia_sdk.payment import PaymentService

PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCeZ7R/6AfLhnbX
V4yikx+3Zk285m70chz7IGev7jHl6SoXM/qQLZGlDmiVz0Llu1fM13Uk/nXk14mP
0Ibj8l127mnl+qvrppifY7RhRhqCoaGJ2mmVmjkkT0GZq31U37ukCh+OMYGO/vFk
M+NP+6X3K8n62KvuXRziVSfL8jYmQFq35bA7jEUNuUwjWHZrV+aiyJXGIev0Is0H
+dXspQhsnz8uWYT7BvxisSMEzNOxFk+M+kILptbLX0rUT7MZ3gFKilOS54O0uuO1
Y0VEeILljP85//p4A4Ha9KH54/YKu96kHSfRuQLuKRKgaIOoEQsX/jEqJJIHcpx4
kh4S8cZxAgMBAAECggEAB6xo6UhNdl3HbIOcd7SuVOVTDztPdS6A+mZVt4dPqf5L
UG/va6QVedwyk01ExZm3dWAbl+Tuw5zwWEPnAOxY/D2s6hvkT6hUnOYI0yyA9MKN
L38h3cIokfp36FCPI/kpnxbxc+MwjkOJ4IuF77Y2UjywDmOIIqYmk81Bvga3+k7Q
vwHMArnl0YXrL4H1Na6fjrsFEyNPeP+n0ItM4LgRRShhXcsM4c84V7rasMfBHFZX
+3WUr3WzY/pZqibSlGW5L1ZvvtyVSD3BTeci8/tWPCMXNnA2cLJRIlsedkU+Ky8m
I0A3O6eSTkdbJzNHJ9RRbx931eN6Y0MDWIXBAZ6g9QKBgQDSLNJd2Mo7MDfmBe44
lGlOHLebcfqF4dsoEcuEG+VP1XyUCS7aq0v/vSfjSu+cJq3F2s0Vn5ZUhFG91iTI
HxHlWUcLsXBQmB4F25fdc+WUc7vR6rIMwMpmE7J/5xFXRroCO/5x97oRsT3xsmwZ
28VrW7kYi0GhlUGlrx8yvulX1QKBgQDA8UdKXFB/wwmjH0c6Vzzf0WT/EtPe65WT
AQRqSXdABV+MBpeSEkb/4Eivk+3gjAEtPgPLopqcTwQ5y9TcPu5AgY03sGmKVYTQ
K5CDKTr1volScMEbbHPYdAqcC3fjnWCFq5qrdb2MrSvYQGwGhrAyS+5qYJHWUhsk
qoRQb6j+LQKBgFai4UiMH7jMRI6OLUenbc0kK09paXKcymE3DKR1d040W3kOXAEJ
kXdm+rVH44ODsigX7GgYc7h9HtDZICpaHF9lMNMSHpEqU13oyi4gIyfRmT+Ltj9p
jUUMo4zzrANFBVH8dwN1sX6viDBEcykpnbSGh8MlTDWWOAxbJsodRkTNAoGAXhvR
qAWLBiY9pyD0fxJaENlzp66pRQwnssJGQwl+bu2wAv6cI5ViqB/flDRVTLc9Q7IB
6+tt+lvYNdCkDKFtWG1YUhdsAxtfYqI9JJyRs5eyJ1Hz/spRXvyKyD4Xxh/XGpvv
Hz6Yq+szfZE+n5hGjOHYcm6T87OspZ++VfWAuikCgYA8A3hJruR8Ic3hq4jo+F7E
2H5jnX6ewnMtwpXfIkWwPf78fDltnEadEz7ocG4E/UjYqh/DGccKoHYbzBAcRCby
0uXg54C5KaYaCa2LFYcwDHhSJfoNbLS7Vxcje3TmgIZ3/VR2PK6gaI2amcy44F+G
o2iSlNxKiuT+yre+uB4+mA==
-----END PRIVATE KEY-----"""

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnme0f+gHy4Z211eMopMf
t2ZNvOZu9HIc+yBnr+4x5ekqFzP6kC2RpQ5olc9C5btXzNd1JP515NeJj9CG4/Jd
du5p5fqr66aYn2O0YUYagqGhidpplZo5JE9Bmat9VN+7pAofjjGBjv7xZDPjT/ul
9yvJ+tir7l0c4lUny/I2JkBat+WwO4xFDblMI1h2a1fmosiVxiHr9CLNB/nV7KUI
bJ8/LlmE+wb8YrEjBMzTsRZPjPpCC6bWy19K1E+zGd4BSopTkueDtLrjtWNFRHiC
5Yz/Of/6eAOB2vSh+eP2CrvepB0n0bkC7ikSoGiDqBELF/4xKiSSB3KceJIeEvHG
cQIDAQAB
-----END PUBLIC KEY-----"""


class TestConfig(unittest.TestCase):

    def test_valid_config(self):
        config = Config(
            api_key="test_api_key",
            pos_signature="test_pos_signature",
            is_live=False,
            notify_url="https://notify_url",
            redirect_url="https://redirect_url",
            public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
            pos_signature_set=["test_pos_signature"]
        )
        self.assertEqual(config.api_key, "test_api_key")
        self.assertEqual(config.base_url, "https://secure-sandbox.netopia-payments.com")

    def test_invalid_config_missing_api_key(self):
        with self.assertRaises(ValueError):
            Config(
                api_key="",
                pos_signature="test_pos_signature",
                is_live=False,
                notify_url="https://notify_url",
                redirect_url="https://redirect_url",
                public_key_str="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
                pos_signature_set=["test_pos_signature"]
            )


class TestPaymentServiceIpn(unittest.TestCase):

    def setUp(self):
        config = Config(
            api_key="test-api-key",
            pos_signature="TEST-POS",
            is_live=False,
            notify_url="https://example.com/ipn",
            redirect_url="https://example.com/return",
            public_key_str=PUBLIC_KEY,
            pos_signature_set=["TEST-POS"],
        )
        client = PaymentClient(config)
        self.payment_service = PaymentService(client)

    def test_verify_ipn_valid(self):
        payload = {
            "payment": {
                "status": 3
            }
        }
        raw_data = json.dumps(payload)

        payload_hash = base64.b64encode(
            hashlib.sha512(raw_data.encode("utf-8")).digest()
        ).decode("utf-8")

        now = datetime.now()

        claims = {
            "iss": "NETOPIA Payments",
            "aud": "TEST-POS",
            "sub": payload_hash,
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp())
        }

        verification_token = encode(
            claims, PRIVATE_KEY, algorithm="RS512"
        )

        mock_request = SimpleNamespace(
            data=raw_data.encode("utf-8"),
            headers={"Verification-token": verification_token}
        )

        result = self.payment_service.verify_ipn(mock_request)

        self.assertEqual(result.status, 3)
        self.assertEqual(result.message, "payment was confirmed; deliver goods")
        self.assertEqual(result.errorType, 0)
        self.assertIsNone(result.errorCode)


if __name__ == '__main__':
    unittest.main()
    
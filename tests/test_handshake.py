import unittest
from src import pq_xdh_handshake_mutual, kyber_keygen, kyber_encapsulate, kyber_decapsulate
from src import falcon_keygen, falcon_sign, falcon_verify

class TestPQXDH(unittest.TestCase):
    def test_key_generation(self):
        """Test Kyber and Falcon key pair generation."""
        pk_kyber_a, _ = kyber_keygen()
        _, sk_falcon_a = falcon_keygen()
        pk_falcon_a, _ = falcon_keygen()

        self.assertEqual(len(pk_kyber_a), 1568, "Kyber public key size mismatch")
        self.assertEqual(len(sk_falcon_a), 2304, "Falcon secret key size mismatch")
        self.assertEqual(len(pk_falcon_a), 1792, "Falcon public key size mismatch")

    def test_encapsulation_decapsulation(self):
        """Test Kyber encapsulation and decapsulation."""
        pk, sk = kyber_keygen()
        ciphertext, shared_secret_enc = kyber_encapsulate(pk)
        shared_secret_dec = kyber_decapsulate(ciphertext, sk)

        self.assertEqual(shared_secret_enc, shared_secret_dec, "Kyber shared secrets do not match")

    def test_signature_verification(self):
        """Test Falcon signing and verification."""
        pk, sk = falcon_keygen()
        message = b"Post-Quantum Test Message"
        signature = falcon_sign(message, sk)

        self.assertTrue(falcon_verify(message, signature, pk), "Falcon signature verification failed")

    def test_full_handshake(self):
        """Test the full post-quantum XDH handshake."""
        valid, ss_alice, ss_bob = pq_xdh_handshake_mutual()

        self.assertTrue(valid, "Handshake authentication failed")
        self.assertEqual(ss_alice, ss_bob, "Handshake shared secrets do not match")

if __name__ == "__main__":
    unittest.main()

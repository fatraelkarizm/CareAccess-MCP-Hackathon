import unittest

from fhir_patient_summary import build_patient_summary


class FhirPatientSummaryTests(unittest.TestCase):
    def test_build_patient_summary_uses_demographics_and_conditions(self):
        patient = {
            "id": "pat-123",
            "name": [{"given": ["Jane"], "family": "Doe"}],
            "gender": "female",
            "birthDate": "1980-01-01",
        }
        conditions = [
            {"code": {"text": "Type 2 Diabetes"}},
            {"code": {"coding": [{"display": "Hypertension"}]}},
        ]

        summary = build_patient_summary(patient, conditions)

        self.assertIn("FHIR Patient/pat-123", summary)
        self.assertIn("Jane Doe", summary)
        self.assertIn("female", summary)
        self.assertIn("born 1980-01-01", summary)
        self.assertIn("Type 2 Diabetes", summary)
        self.assertIn("Hypertension", summary)

    def test_build_patient_summary_handles_missing_fields(self):
        summary = build_patient_summary({"id": "pat-456"}, [])

        self.assertIn("FHIR Patient/pat-456", summary)
        self.assertIn("name unavailable", summary)
        self.assertIn("Conditions: none available", summary)

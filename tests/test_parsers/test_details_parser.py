import pytest
from src.parsers.details_parser import DetailsParser

def test_parse_basic_info(sample_school_html):
    """Test parsing basic school information."""
    parser = DetailsParser(sample_school_html)
    info = parser.parse_basic_info()
    
    assert info["id"] == "123456"
    assert info["name"] == "Test School"
    assert info["phone"] == "123456789"
    assert info["fax"] == "987654321"
    assert info["email"] == "test.school@example.com"
    assert info["website"] == "www.example.com"

def test_parse_location_info(sample_school_html):
    """Test parsing school location information."""
    parser = DetailsParser(sample_school_html)
    info = parser.parse_location_info()
    
    assert info["autonomous_community"] == "Test Autonomous Community"
    assert info["province"] == "Test Province"
    assert info["country"] == "ESPAÑA"
    assert info["region"] == ""
    assert info["sub_region"] == ""
    assert info["municipality"] == "Test City"
    assert info["locality"] == "Test City"
    assert info["address"] == "Test Street 123"
    assert info["postal_code"] == "12345"

def test_parse_classification_info(sample_school_html):
    """Test parsing school classification information."""
    parser = DetailsParser(sample_school_html)
    info = parser.parse_classification_info()
    
    assert info["nature"] == "Centro público"
    assert info["is_concerted"] == "No"
    assert info["center_type"] == "Colegio Público"
    assert info["generic_name"] == "Colegio de Educación Infantil y Primaria"

def test_parse_services(sample_school_html):
    """Test parsing school services."""
    parser = DetailsParser(sample_school_html)
    services = parser.parse_services()
    
    assert "Comedor" in services
    assert "Transporte" in services
    assert "Biblioteca" in services
    assert "Gimnasio" in services

def test_parse_imparted_studies(sample_school_html):
    """Test parsing imparted studies."""
    parser = DetailsParser(sample_school_html)
    studies = parser.parse_imparted_studies()
    
    assert len(studies) == 3
    for study in studies:
        assert isinstance(study, dict)
        assert "name" in study
        assert "degree" in study
        assert "family" in study
        assert "modality" in study
        assert all(isinstance(value, str) for value in study.values())

def test_parse_all(sample_school_html):
    """Test parsing all school information."""
    parser = DetailsParser(sample_school_html)
    info = parser.parse_all()
    
    # Check that all sections are present
    assert "id" in info
    assert "name" in info
    assert "phone" in info
    assert "fax" in info
    assert "email" in info
    assert "website" in info
    assert "autonomous_community" in info
    assert "province" in info
    assert "country" in info
    assert "region" in info
    assert "sub_region" in info
    assert "municipality" in info
    assert "locality" in info
    assert "address" in info
    assert "postal_code" in info
    assert "nature" in info
    assert "is_concerted" in info
    assert "center_type" in info
    assert "generic_name" in info
    assert "services" in info
    assert "imparted_studies" in info

def test_parse_with_invalid_html():
    """Test parsing with invalid HTML."""
    parser = DetailsParser("<invalid>html</invalid>")
    
    # Should handle invalid HTML gracefully
    info = parser.parse_all()
    assert info["id"] is None
    assert info["name"] is None
    assert info["services"] == []
    assert info["imparted_studies"] == [] 
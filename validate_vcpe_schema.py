#!/usr/bin/env python3
"""
Script de validació de l'esquema JSON TRZ per ICATMAR
Valida payloads contra l'esquema definit i realitza tests de seguretat
"""

import json
import jsonschema
from jsonschema import validate, ValidationError, Draft202012Validator
import sys
from typing import Dict, Any, List
from datetime import datetime


class TRZValidator:
    """Validador per a esquemes TRZ amb comprovacions de seguretat"""
    
    def __init__(self, schema_path: str):
        """
        Inicialitza el validador amb l'esquema JSON
        
        Args:
            schema_path: Ruta al fitxer d'esquema JSON
        """
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
        
        # Crear validador
        self.validator = Draft202012Validator(self.schema)
    
    def validate_payload(self, payload: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valida un payload contra l'esquema
        
        Args:
            payload: Diccionari amb les dades a validar
            
        Returns:
            Tupla (és_vàlid, llista_errors)
        """
        errors = []
        
        try:
            # Validació principal amb JSON Schema
            self.validator.validate(payload)
            
            # Validacions de negoci addicionals
            business_errors = self._validate_business_rules(payload)
            if business_errors:
                errors.extend(business_errors)
                return False, errors
            
            # Validacions de seguretat
            security_errors = self._validate_security(payload)
            if security_errors:
                errors.extend(security_errors)
                return False, errors
                
            return True, []
            
        except ValidationError as e:
            errors.append(f"Error de validació: {e.message}")
            errors.append(f"  Ruta: {' -> '.join(str(p) for p in e.path)}")
            return False, errors
        except Exception as e:
            errors.append(f"Error inesperat: {str(e)}")
            return False, errors
    
    def _validate_business_rules(self, payload: Dict[str, Any]) -> List[str]:
        """
        Valida regles de negoci específiques
        
        Args:
            payload: Dades a validar
            
        Returns:
            Llista d'errors detectats
        """
        errors = []
        
        # Validar que les dates de captura siguin anteriors a la venda
        if 'EstablecimientosVenta' in payload:
            for estab in payload['EstablecimientosVenta'].get('EstablecimientoVenta', []):
                for venta in estab.get('Ventas', {}).get('VentasUnidadProductiva', []):
                    for especie in venta.get('Especies', {}).get('Especie', []):
                        fecha_venta = especie.get('FechaVenta')
                        
                        # Comprovar dates de captura
                        fechas_captura = especie.get('FechasCaptura', {}).get('FechaCaptura', [])
                        for fc in fechas_captura:
                            fecha_ini = fc.get('FechaCapturaIni')
                            fecha_fin = fc.get('FechaCapturaFin')
                            
                            if fecha_ini and fecha_venta:
                                if fecha_ini > fecha_venta:
                                    errors.append(
                                        f"FechaCapturaIni ({fecha_ini}) posterior a FechaVenta ({fecha_venta})"
                                    )
                            
                            if fecha_fin and fecha_venta:
                                if fecha_fin > fecha_venta:
                                    errors.append(
                                        f"FechaCapturaFin ({fecha_fin}) posterior a FechaVenta ({fecha_venta})"
                                    )
                            
                            if fecha_ini and fecha_fin:
                                if fecha_ini > fecha_fin:
                                    errors.append(
                                        f"FechaCapturaIni ({fecha_ini}) posterior a FechaCapturaFin ({fecha_fin})"
                                    )
        
        return errors
    
    def _validate_security(self, payload: Dict[str, Any]) -> List[str]:
        """
        Comprovacions de seguretat addicionals
        
        Args:
            payload: Dades a validar
            
        Returns:
            Llista d'alertes de seguretat
        """
        errors = []
        
        # Comprovar patrons sospitosos (SQL injection, XSS, etc.)
        suspicious_patterns = [
            "'; DROP TABLE",
            "<script>",
            "javascript:",
            "onerror=",
            "onload=",
            "../",
            "<?php",
            "${",
            "exec(",
            "eval(",
        ]
        
        def check_string_fields(obj: Any, path: str = "root"):
            """Comprova recursivament tots els strings per patrons sospitosos"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    check_string_fields(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_string_fields(item, f"{path}[{i}]")
            elif isinstance(obj, str):
                for pattern in suspicious_patterns:
                    if pattern.lower() in obj.lower():
                        errors.append(
                            f"ALERTA SEGURETAT: Patró sospitós '{pattern}' detectat a {path}"
                        )
        
        check_string_fields(payload)
        
        return errors
    
    def validate_file(self, file_path: str) -> tuple[bool, List[str]]:
        """
        Valida un fitxer JSON
        
        Args:
            file_path: Ruta al fitxer JSON a validar
            
        Returns:
            Tupla (és_vàlid, llista_errors)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
            return self.validate_payload(payload)
        except json.JSONDecodeError as e:
            return False, [f"Error llegint JSON: {str(e)}"]
        except FileNotFoundError:
            return False, [f"Fitxer no trobat: {file_path}"]


def run_security_tests():
    """Executa una bateria de tests de seguretat"""
    
    print("\n" + "="*80)
    print("TESTS DE SEGURETAT")
    print("="*80 + "\n")
    
    validator = TRZValidator('vcpe-schema.json')
    
    # Test 1: SQL Injection
    print("Test 1: Injecció SQL...")
    sql_injection_payload = {
        "NumEnvio": "ENV001'; DROP TABLE ventas; --",
        "TipoRespuesta": 1
    }
    valid, errors = validator.validate_payload(sql_injection_payload)
    if not valid:
        print("  ✓ PROTEGIT: SQL injection detectat i bloquejat")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  ✗ VULNERABLE: SQL injection no detectat!")
    
    # Test 2: XSS
    print("\nTest 2: Cross-Site Scripting (XSS)...")
    xss_payload = {
        "NumEnvio": "ENV001",
        "TipoRespuesta": 1,
        "EstablecimientosVenta": {
            "EstablecimientoVenta": [{
                "NumIdentificacionEstablec": "<script>alert('xss')</script>",
                "Ventas": {
                    "VentasUnidadProductiva": []
                }
            }]
        }
    }
    valid, errors = validator.validate_payload(xss_payload)
    if not valid:
        print("  ✓ PROTEGIT: XSS detectat i bloquejat")
        for error in errors[:3]:  # Mostrar només primers 3 errors
            print(f"    - {error}")
    else:
        print("  ✗ VULNERABLE: XSS no detectat!")
    
    # Test 3: Path Traversal
    print("\nTest 3: Path Traversal...")
    path_traversal_payload = {
        "NumEnvio": "ENV001",
        "TipoRespuesta": 1,
        "EstablecimientosVenta": {
            "EstablecimientoVenta": [{
                "NumIdentificacionEstablec": "../../../etc/passwd",
                "Ventas": {
                    "VentasUnidadProductiva": []
                }
            }]
        }
    }
    valid, errors = validator.validate_payload(path_traversal_payload)
    if not valid:
        print("  ✓ PROTEGIT: Path traversal detectat i bloquejat")
    else:
        print("  ✗ VULNERABLE: Path traversal no detectat!")
    
    # Test 4: Payload massiu (DoS)
    print("\nTest 4: DoS amb array massiu...")
    dos_payload = {
        "NumEnvio": "ENV001",
        "TipoRespuesta": 1,
        "EstablecimientosVenta": {
            "EstablecimientoVenta": [
                {
                    "NumIdentificacionEstablec": f"EST{i:06d}",
                    "Ventas": {"VentasUnidadProductiva": []}
                }
                for i in range(150)  # Més del maxItems: 100
            ]
        }
    }
    valid, errors = validator.validate_payload(dos_payload)
    if not valid:
        print("  ✓ PROTEGIT: Array massiu detectat i bloquejat")
    else:
        print("  ✗ VULNERABLE: DoS amb array massiu no detectat!")
    
    # Test 5: Camps addicionals no esperats
    print("\nTest 5: Property pollution amb camps inesperats...")
    pollution_payload = {
        "NumEnvio": "ENV001",
        "TipoRespuesta": 1,
        "__proto__": {"admin": True},
        "constructor": {"prototype": {"admin": True}}
    }
    valid, errors = validator.validate_payload(pollution_payload)
    if not valid:
        print("  ✓ PROTEGIT: Property pollution detectat i bloquejat")
    else:
        print("  ✗ VULNERABLE: Property pollution no detectat!")
    
    print("\n" + "="*80 + "\n")


def main():
    """Funció principal"""
    
    print("\n" + "="*80)
    print("VALIDADOR D'ESQUEMA JSON TRZ - ICATMAR")
    print("Treball Fi de Màster - Ciberseguretat i Privadesa")
    print("="*80 + "\n")
    
    # Validar esquema
    print("Carregant esquema...")
    try:
        validator = TRZValidator('vcpe-schema.json')
        print("✓ Esquema carregat correctament\n")
    except Exception as e:
        print(f"✗ Error carregant esquema: {e}")
        sys.exit(1)
    
    # Validar exemple vàlid
    print("="*80)
    print("VALIDACIÓ D'EXEMPLE VÀLID")
    print("="*80 + "\n")
    
    print("Validant validate_vcpe_schema.py...")
    valid, errors = validator.validate_file('validate_vcpe_schema.py')
    
    if valid:
        print("✓ Payload VÀLID")
        print("  Totes les validacions passades correctament")
    else:
        print("✗ Payload INVÀLID")
        print("\nErrors detectats:")
        for error in errors:
            print(f"  - {error}")
    
    # Tests de seguretat
    run_security_tests()
    
    # Resum
    print("="*80)
    print("RESUM DE VALIDACIÓ")
    print("="*80)
    print(f"Data execució: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Esquema validat: vcpe-schema.json")
    print(f"Versió esquema: 1.0.0")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
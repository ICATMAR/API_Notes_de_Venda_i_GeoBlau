Envio
├── NumEnvio (requerit)
├── TipoRespuesta
└── EstablecimientosVenta
    └── EstablecimientoVenta[]
        ├── NumIdentificacionEstablec (requerit)
        └── Ventas
            └── VentasUnidadProductiva[]
                ├── DatosUnidadProductiva (oneOf)
                │   ├── Buque
                │   ├── Granja
                │   └── PersonaFisJur
                └── Especies
                    └── Especie[]
                        ├── NumDocVenta (requerit)
                        ├── EspecieAL3 (requerit)
                        ├── FechaVenta (requerit)
                        ├── ... (més camps)
                        └── Observaciones
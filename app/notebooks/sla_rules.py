"""Regras canônicas de SLA compartilhadas pelas tabelas Gold do app."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

PCT_ESCALONAMENTO_GESTOR = 0.40
PCT_ESCALONAMENTO_ADMIN = 0.70
PCT_PROXIMO_VENCIMENTO = PCT_ESCALONAMENTO_ADMIN
PCT_SLA_VENCIDO = 1.00


def intervalo_para_segundos(coluna):
    """Converte intervalos JDBC em HH:MM[:SS] ou texto de unidade PostgreSQL."""
    valor = F.lower(F.trim(coluna.cast("string")))
    hhmm = valor.rlike(r"^-?\d+:\d{1,2}(:\d{1,2}(\.\d+)?)?$")
    horas_hhmm = F.regexp_extract(valor, r"^(-?\d+):", 1).cast("double")
    minutos_hhmm = F.regexp_extract(valor, r"^-?\d+:(\d{1,2})", 1).cast("double")
    segundos_hhmm = F.regexp_extract(valor, r"^-?\d+:\d{1,2}:(\d{1,2}(\.\d+)?)$", 1).cast("double")
    horas_txt = F.regexp_extract(valor, r"(-?\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\b", 1).cast("double")
    minutos_txt = F.regexp_extract(valor, r"(-?\d+(?:\.\d+)?)\s*(?:minutes?|mins?)\b", 1).cast("double")
    segundos_txt = F.regexp_extract(valor, r"(-?\d+(?:\.\d+)?)\s*(?:seconds?|secs?)\b", 1).cast("double")
    horas = F.when(hhmm, horas_hhmm).otherwise(F.coalesce(horas_txt, F.lit(0.0)))
    minutos = F.when(hhmm, minutos_hhmm).otherwise(F.coalesce(minutos_txt, F.lit(0.0)))
    segundos = F.when(hhmm, F.coalesce(segundos_hhmm, F.lit(0.0))).otherwise(F.coalesce(segundos_txt, F.lit(0.0)))
    reconhecido = valor.isNotNull() & (hhmm | valor.rlike(r"hours?|hrs?|minutes?|mins?|seconds?|secs?"))
    return F.when(reconhecido, horas * 3600 + minutos * 60 + segundos)


def adicionar_campos_sla(df: DataFrame, incluir_minutos_restantes: bool = False) -> DataFrame:
    """Acrescenta percentual consumido, estado e etapa prevista do SLA."""
    fim_contagem = F.coalesce(F.col("data_hora_resolucao"), F.current_timestamp())
    resultado = (
        df.withColumn("vida_util_referencia_segundos", intervalo_para_segundos(F.col("vida_util_referencia_horas")))
        .withColumn(
            "tempo_decorrido_segundos",
            F.greatest(F.lit(0), F.unix_timestamp(fim_contagem) - F.unix_timestamp("data_hora_alerta")),
        )
        .withColumn(
            "percentual_consumido_sla",
            F.when(
                F.col("vida_util_referencia_segundos") > 0,
                F.round(F.col("tempo_decorrido_segundos") / F.col("vida_util_referencia_segundos"), 4),
            ),
        )
        .withColumn(
            "estado_sla",
            F.when(
                F.col("vida_util_referencia_segundos").isNull()
                | (F.col("vida_util_referencia_segundos") <= 0)
                | F.col("percentual_consumido_sla").isNull(),
                "SEM_REFERENCIA",
            )
            .when(F.col("percentual_consumido_sla") >= F.lit(PCT_SLA_VENCIDO), "SLA_VENCIDO")
            .when(F.col("percentual_consumido_sla") >= F.lit(PCT_PROXIMO_VENCIMENTO), "PROXIMO_VENCIMENTO")
            .otherwise("NO_PRAZO"),
        )
        .withColumn(
            "etapa_escalonamento",
            F.when(F.col("estado_sla") == "SEM_REFERENCIA", "SEM_REFERENCIA")
            .when(F.col("percentual_consumido_sla") >= F.lit(PCT_SLA_VENCIDO), "SLA_VENCIDO")
            .when(F.col("percentual_consumido_sla") >= F.lit(PCT_ESCALONAMENTO_ADMIN), "ADMIN")
            .when(F.col("percentual_consumido_sla") >= F.lit(PCT_ESCALONAMENTO_GESTOR), "GESTOR")
            .otherwise("OPERADOR"),
        )
    )
    if incluir_minutos_restantes:
        resultado = resultado.withColumn(
            "minutos_restantes_sla",
            F.when(
                F.col("vida_util_referencia_segundos") > 0,
                F.ceil((F.col("vida_util_referencia_segundos") - F.col("tempo_decorrido_segundos")) / 60),
            ),
        )
    return resultado

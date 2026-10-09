"""Punto de entrada único de la CLI."""

from __future__ import annotations

import argparse
import sys

from renovable.controllers import composicion
from renovable.controllers.cli.comandos import build, extract, regulatorio, verificar, vigencia


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="renovable",
        description="Informe ejecutivo de energías renovables (MinMinas -> Cancillería)",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_reg = sub.add_parser("regulatorio", help="estado de la evidencia regulatoria (CREG)")
    p_reg.set_defaults(func=lambda args: regulatorio.ejecutar(composicion.construir(dibujar=False)))

    p_ext = sub.add_parser("extract", help="ejecuta el SQL y puebla la caché")
    p_ext.add_argument("--refrescar", action="store_true", help="vuelve a consultar la base")
    p_ext.set_defaults(
        func=lambda args: extract.ejecutar(composicion.construir(dibujar=False), args.refrescar)
    )

    p_ver = sub.add_parser("verificar", help="valida el informe sin exportar")
    p_ver.add_argument("--refrescar", action="store_true")
    p_ver.set_defaults(
        func=lambda args: verificar.ejecutar(composicion.construir(dibujar=False), args.refrescar)
    )

    p_build = sub.add_parser("build", help="compone el informe y exporta el PDF")
    p_build.add_argument("--refrescar", action="store_true", help="vuelve a consultar la base")
    p_build.set_defaults(
        func=lambda args: build.ejecutar(composicion.construir(dibujar=True), args.refrescar)
    )

    p_vig = sub.add_parser(
        "vigencia", help="verifica que la evidencia regulatoria sea la más reciente"
    )
    p_vig.add_argument("--dias", type=int, default=30, help="antigüedad máxima aceptada")
    p_vig.set_defaults(
        func=lambda args: vigencia.ejecutar(composicion.construir(dibujar=False), args.dias)
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

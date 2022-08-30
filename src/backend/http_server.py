from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.services import influx_service

from .controllers import AuthConfig, AuthController, WorkstationController
from .exceptions import AuthenticatorServiceException, InvalidCredentialsError
from .routers import AuthRouterBuilder, WorkstationRouterBuilder
from .services.db_service import DBConfig, DBService
from .services.influx_service import InfluxConfig, InfluxService


@dataclass
class APIConfig:
    addr: str
    port: int


NOT_SECURED_PATHS = [
    "/login",
    "/signup",
]


@dataclass
class HTTPServer:
    authconfig: AuthConfig
    dbconfig: DBConfig
    influxconfig: InfluxConfig

    def build_app(self) -> FastAPI:  # noqa: C901
        app = FastAPI(title="HTTP keyserver", version="0.1")
        dbservice: DBService = DBService(self.dbconfig)
        influx_service: InfluxService = InfluxService(self.influxconfig)

        authController: AuthController = AuthController(self.authconfig)
        workstationController: WorkstationController = WorkstationController(
            dbservice, influx_service
        )

        @app.middleware("http")
        async def authMiddleware(request: Request, call_next):
            print("authMiddleware")

            if (
                request.scope["path"] in NOT_SECURED_PATHS
                or self.authconfig.mode == "OFF"
            ):
                response = await call_next(request)
                return response
            else:
                try:
                    cookie = request.cookies["Authorization"]
                except Exception:
                    return JSONResponse("Authorization cookie missing", 401)
                try:
                    if authController.validate(cookie):
                        response = await call_next(request)
                    else:
                        JSONResponse("Wrong email or password", 401)
                except InvalidCredentialsError as e:
                    return JSONResponse(e.detail, 401)
                except AuthenticatorServiceException as e:
                    return JSONResponse(e.detail, 500)

            return response

        routers = {
            AuthRouterBuilder(authController),
            WorkstationRouterBuilder(workstationController),
        }

        for router in routers:
            app.include_router(router.build())

        @app.get("/authtest")
        async def dbtest():
            return "authorized"

        return app
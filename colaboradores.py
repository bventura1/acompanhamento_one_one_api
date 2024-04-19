from sqlalchemy import Column, Integer, String
from typing import Union
from  model import Base


class Colaboradores(Base):
    __tablename__ = 'colaboradores'

    id = Column("pk_atividade", Integer, primary_key=True)
    nome = Column(String(140))
    cargo = Column(String(140))

    def __init__(self, nome:str, cargo:str,):
        """
        Cadastro de Colaboradores

        """

        self.nome = nome
        self.cargo = cargo
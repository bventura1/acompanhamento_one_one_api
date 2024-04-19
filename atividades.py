from sqlalchemy import Column, Integer, String, DateTime#, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Atividades(Base):
    __tablename__ = 'atividades'

    id = Column("pk_atividade", Integer, primary_key=True)
    tarefa = Column(String(140))
    colaborador = Column(String(140))#, ForeignKey("colaborador.nome"), nullable=False)
    status = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, tarefa:str, colaborador:str, status:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria as tarefas que cada um terá como responsabilidade

        """
        self.tarefa = tarefa
        self.colaborador = colaborador
        self.status = status

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao



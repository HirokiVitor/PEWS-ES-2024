from .models import Paciente, Avaliacao
from datetime import datetime

class TriagemService:
    """
    Classe Facade para simplificar operações de Paciente e Avaliação
    """

    @staticmethod
    def cadastrar_paciente(nome, idade, leito, dih, diagnostico, data_internacao=None):
        if data_internacao is None:
            data_internacao = datetime.now()  # Define a data se não for informada

        return Paciente.objects.create(
            nome=nome, idade=idade, leito=leito, dih=dih, diagnostico=diagnostico, data_internacao=data_internacao
        )

    @staticmethod
    def registrar_avaliacao(paciente_id, score, freq_cardiaca, freq_respiratoria, 
                            analise, av_neuro, av_cardio, av_resp, extras):
        """
        Registra uma nova avaliação para um paciente existente.
        """
        paciente = Paciente.objects.get(id=paciente_id)
        return Avaliacao.objects.create(
            paciente=paciente,
            score=score,
            freq_cardiaca=freq_cardiaca,
            freq_respiratoria=freq_respiratoria,
            analise=analise,
            av_neuro=av_neuro,
            av_cardio=av_cardio,
            av_resp=av_resp,
            extras=extras
        )

    @staticmethod
    def dar_alta_paciente(paciente_id):
        """
        Marca um paciente como inativo no sistema (dar alta).
        """
        paciente = Paciente.objects.get(id=paciente_id)
        paciente.delete()
        return f"{paciente.nome} recebeu alta com sucesso!"

    @staticmethod
    def listar_pacientes_ativos():
        """
        Retorna a lista de pacientes ativos.
        """
        return Paciente.objects.all()

    @staticmethod
    def obter_historico_avaliacoes(paciente_id):
        """
        Retorna o histórico de avaliações de um paciente.
        """
        paciente = Paciente.objects.get(id=paciente_id)
        return paciente.avaliacoes.all().order_by('-data')

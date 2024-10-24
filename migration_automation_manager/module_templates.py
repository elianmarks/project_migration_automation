# -*- coding: utf-8 -*-
"""


- Contributors
Elliann Marks <elian.markes@gmail.com>

- Version 02 - 07/08/2019
Functions -
Libraries -
Dependencies - ModuleLog class

"""


class ModuleTemplates:

    def __init__(self, module_log):
        self._log = module_log
        self.ns_zones = None
        self.destination_ip = None
        self.info_list = None
        self.this_owner = None
        self.brand = None

    def turbo_completed(self, ns_zones, destination_ip, brand="br"):
        try:
            self.brand = brand
            self.ns_zones = ns_zones
            self.destination_ip = destination_ip
            if self.brand == "br":
                return "Olá" \
                   "\n\nTemos boas notícias! A migração solicitada foi realizada com sucesso!" \
                   "\n\nPor favor, nos retorne nas próximas 48 horas caso encontre algum problema ou necessite de algo relacionado a esta migração." \
                   "\n\nÉ necessário que nesse momento altere as DNS onde registrou o domínio para as seguintes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nO novo IP do(s) domínio(s) da sua conta compartilhada é {}." \
                   "\n\nMantivemos um apontamento interno que se manterá nas próximas 48 horas. Assim, até que altere as DNS nesse período, todo o tráfego do seu site está sendo direcionado para o novo servidor." \
                   "\n\nNão se preocupe, pois isso garante a preservação de todos os dados entre esse período." \
                   "\n\nConte sempre conosco!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""), self.destination_ip)
            elif self.brand == "es":
                return "Hola" \
                   "\n\nTenemos buenas noticias! La migración solicitada ha sido realizada con éxito!" \
                   "\n\nPor favor, infórmenos en las próximas 48 horas si encuantras algún problema o necesitas algo relativo a esta migración." \
                   "\n\nEs necesario que en este momento alteres los DNS donde registró el dominio para los siguientes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nEl nuevo IP del(los) dominio(s) de su cuenta compartida es {}." \
                   "\n\nMantuvimos un apuntamiento interno que estará activo durante las próximas 48 horas. Así, hasta que alteres los DNS en ese período, todo el tráfico de tu sitio estará siendo direccionado para el nuevo servidor." \
                   "\n\nNo te preocupes, pues esto garantiza la preservación de todos los datos en este periodo." \
                   "\n\nCuenta siempre con nosotros!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""), self.destination_ip)
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def shared_completed(self, ns_zones, brand="br"):
        try:
            self.brand = brand
            self.ns_zones = ns_zones
            if self.brand == "br":
                return "Olá" \
                   "\n\nA migração foi realizada com sucesso!" \
                   "\n\nPor favor, nos retorne nas próximas 48 horas caso encontre algum problema ou necessite de algo relacionado a esta migração." \
                   "\n\nÉ necessário que nesse momento altere as DNS onde registrou o domínio para as seguintes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantivemos um apontamento de DNS interno. Assim, até que altere as DNS, todo o tráfego do seu site está sendo direcionado para o novo servidor." \
                   "\n\nConte sempre conosco!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            elif self.brand == "es":
                return "Hola" \
                   "\n\nLa migración solicitada ha sido realizada con éxito!" \
                   "\n\nPor favor, infórmenos en las próximas 48 horas si encuantras algún problema o necesitas algo relativo a esta migración." \
                   "\n\nEs necesario que en este momento alteres los DNS donde registró el dominio para los siguientes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantuvimos un apuntamiento interno que estará activo durante las próximas 48 horas. Así, hasta que alteres los DNS en ese período, todo el tráfico de tu sitio estará siendo direccionado para el nuevo servidor." \
                   "\n\nCuenta siempre con nosotros!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def reseller_completed(self, ns_zones, brand="br"):
        try:
            self.brand = brand
            self.ns_zones = ns_zones
            if self.brand == "br":
                return "Olá" \
                   "\n\nA migração foi realizada com sucesso!" \
                   "\n\nPor favor, nos retorne nas próximas 48 horas caso encontre algum problema ou necessite de algo relacionado a esta migração." \
                   "\n\nÉ necessário que nesse momento altere as DNS onde registrou o domínio para as seguintes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantivemos um apontamento de DNS interno. Assim, até que altere as DNS, todo o tráfego do seu site está sendo direcionado para o novo servidor." \
                   "\n\nConte sempre conosco!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            elif self.brand == "es":
                return "Hola" \
                   "\n\nLa migración solicitada ha sido realizada con éxito!" \
                   "\n\nPor favor, infórmenos en las próximas 48 horas si encuantras algún problema o necesitas algo relativo a esta migración." \
                   "\n\nEs necesario que en este momento alteres los DNS donde registró el dominio para los siguientes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantuvimos un apuntamiento interno que estará activo durante las próximas 48 horas. Así, hasta que alteres los DNS en ese período, todo el tráfico de tu sitio estará siendo direccionado para el nuevo servidor." \
                   "\n\nCuenta siempre con nosotros!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def allusers_completed(self, ns_zones, brand="br"):
        try:
            self.brand = brand
            self.ns_zones = ns_zones
            if self.brand == "br":
                return "Olá" \
                   "\n\nA migração foi realizada com sucesso!" \
                   "\n\nPor favor, nos retorne nas próximas 48 horas caso encontre algum problema ou necessite de algo relacionado a esta migração." \
                   "\n\nÉ necessário que nesse momento altere as DNS onde registrou o domínio para as seguintes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantivemos um apontamento de DNS interno. Assim, até que altere as DNS, todo o tráfego do seu site está sendo direcionado para o novo servidor." \
                   "\n\nConte sempre conosco!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            elif self.brand == "es":
                return "Hola" \
                   "\n\nLa migración solicitada ha sido realizada con éxito!" \
                   "\n\nPor favor, infórmenos en las próximas 48 horas si encuantras algún problema o necesitas algo relativo a esta migración." \
                   "\n\nEs necesario que en este momento alteres los DNS donde registró el dominio para los siguientes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantuvimos un apuntamiento interno que estará activo durante las próximas 48 horas. Así, hasta que alteres los DNS en ese período, todo el tráfico de tu sitio estará siendo direccionado para el nuevo servidor." \
                   "\n\nCuenta siempre con nosotros!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def monitoring_completed(self, ns_zones, destination_ip, brand="br"):
        try:
            self.brand = brand
            self.ns_zones = ns_zones
            self.destination_ip = destination_ip
            if self.brand == "br":
                return "Olá" \
                   "\n\nA migração foi realizada com sucesso!" \
                   "\n\nPor favor, nos retorne nas próximas 48 horas caso encontre algum problema ou necessite de algo relacionado a esta migração." \
                   "\n\nÉ necessário que nesse momento altere as DNS onde registrou o domínio para as seguintes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nO novo IP do(s) domínio(s) da sua conta compartilhada é {}." \
                   "\n\nMantivemos um apontamento interno que se manterá nas próximas 48 horas. Assim, até que altere as DNS nesse período, todo o tráfego do seu site está sendo direcionado para o novo servidor." \
                   "\n\nNão se preocupe, pois isso garante a preservação de todos os dados entre esse período." \
                   "\n\nConte sempre conosco!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""), self.destination_ip)
            elif self.brand == "es":
                return "Hola" \
                   "\n\nLa migración solicitada ha sido realizada con éxito!" \
                   "\n\nPor favor, infórmenos en las próximas 48 horas si encuantras algún problema o necesitas algo relativo a esta migración." \
                   "\n\nEs necesario que en este momento alteres los DNS donde registró el dominio para los siguientes:" \
                   "\n\nNS1: {}" \
                   "\n\nNS2: {}" \
                   "\n\nMantuvimos un apuntamiento interno que estará activo durante las próximas 48 horas. Así, hasta que alteres los DNS en ese período, todo el tráfico de tu sitio estará siendo direccionado para el nuevo servidor." \
                   "\n\nCuenta siempre con nosotros!".format(self.ns_zones[0].replace("ns=", ""), self.ns_zones[1].replace("ns=", ""))
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def all_started(self, brand="br"):
        try:
            self.brand = brand
            if self.brand == "br":
                return "Olá, tudo bem?" \
                   "\n\nOlha só, queremos lhe informar que iniciamos neste momento a migração e assim que finalizar iremos lhe avisar através deste mesmo chamado, ok?" \
                   "\n\nO processo todo pode levar até no máximo 24hrs úteis, mas costumamos finalizar bem antes!" \
                   "\n\nEntão de agora em diante, pedimos que não faça nenhuma alteração para evitar que durante o processo de transferência os seus arquivos fiquem desatualizados." \
                   "\n\nSe tiver alguma dúvida estamos à sua disposição!" \
                   "\n\nForte abraço!"
            elif self.brand == "es":
                return "Hola, todo bien?" \
                   "\n\n Nos gustaría informarle que en este momento hemos iniciado la migración y al momento de finalizar le estaremos notificando por esta misma vía, ok?" \
                   "\n\n El proceso puede tardar hasta 24 horas útiles, sin embargo acostumbramos a finalizar antes de ese plazo!" \
                   "\n\n Le pedimos por favor que no haga ninguna modificación en su sitio, para evitar que durante el proceso de transferencia sus archivos sean desactualizados." \
                   "\n\n En caso de tener alguna duda estamos a su disposición para aclarar!" \
                   "\n\n Reciba un fuerte abrazo!"
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))

    def not_ns(self, brand="br"):
        try:
            self.brand = brand
            if self.brand == "br":
                return "Olá, tudo bem?" \
                   "\n\nIdentificamos que o seu domínio não está apontando para o servidor NS da sua conta, assim gostaríamos de alertar que após a " \
                   "migração será necessário atualizar o IP na zona do seu domínio no servidor NS utilizado, ao contrário seus serviços irão ficar fora do ar." \
                   "\n\nDessa forma, peço que autorize o início da migração ou informe um melhor horário e data para que a migração seja realizada." \
                   "\n\nFicamos no seu aguardo para prosseguirmos." \
                   "\n\nSe tiver alguma dúvida estamos à sua disposição!" \
                   "\n\nForte abraço!"
            elif self.brand == "es":
                return "Hola, todo bien?" \
                   "\n\nIdentificamos que su domínio no está apuntando para el servidor NS de su cuenta, así, nos gustaría alertarte que luego de la" \
                   "migración será necesario actualizar la IP en la zona DNS de su dominio dentro del servidor NS utilizado, de lo contrario, sus servicios irán a quedar offline." \
                   "\n\nDe esta forma, pido que nos autorice el inicio de la migración o nos informe el mejor horario y día para realizar esto." \
                   "\n\nQuedamos a su espera para proseguir." \
                   "\n\nSi tienes alguna duda estamos a disposición!" \
                   "\n\nFuerte abrazo!"
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def turbo_started(self, brand="br"):
        try:
            self.brand = brand
            if self.brand == "br":
                return "Olá, tudo bem?" \
                   "\n\nEstamos super felizes que você esteja mudando para o nosso plano Turbo, isso quer dizer que seu projeto está crescendo, não é mesmo? =)" \
                   "\n\nOlha só, queremos lhe informar que iniciamos neste momento a transferência dos seus arquivos para o seu novo plano e assim que finalizar iremos lhe avisar através deste mesmo chamado, ok?" \
                   "\n\nO processo todo pode levar até no máximo 24hrs úteis, mas costumamos finalizar bem antes!" \
                   "\n\nEntão de agora em diante, pedimos que não faça nenhuma alteração no seu plano atual para evitar que durante o processo de transferência os seus arquivos fiquem desatualizados no Turbo." \
                   "\n\nSe tiver alguma dúvida estamos à sua disposição!" \
                   "\n\nForte abraço!"
            elif self.brand == "es":
                return "Hola, todo bien?" \
                   "\n\n Estamos super felices que estés mudando para nuestro plan Turbo, Esto quiere decir que tu proyecto está creciendo, cierto? =)" \
                   "\n\nMira, queremos informarte que iniciamos en este momento la transferencia de tus archivos para tu nuevo plan y así que finalicemos te avisaremos a través de este mismo llamado, ok?" \
                   "\n\nTodo el proceso puede llevar hasta 24 horas útiles aunque acostumbramos finalizar antes!" \
                   "\n\nEntonces, de ahora en adelante pedimos que no realices ninguna alteración en tu plan actual para evitar que durante el proceso de transferencia de archivos se desactualicen en el Turbo." \
                   "\n\nSi tienes alguna duda estamos a disposición!" \
                   "\n\nFuerte abrazo!"
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def monitoring_started(self, brand="br"):
        try:
            self.brand = brand
            if self.brand == "br":
                return "Olá," \
                   "\n\nIniciamos neste momento a migração de suas contas." \
                   "\n\nPedimos, por gentileza, que não faça nenhuma alteração até a conclusão da migração, tais como troca de senha ou utilização de FTP." \
                   "\n\nNão temos uma estimativa do tempo para finalizar o processo, contudo enviaremos uma notificação assim que for concluído." \
                   "\n\nRetornaremos em breve." \
                   "\n\nSe tiver alguma dúvida estamos à sua disposição!" \
                   "\n\nForte abraço!"
            elif self.brand == "es":
                return "Hola," \
                   "\n\nIniciamos en este momento la migración de tus cuentas." \
                   "\n\nPedimos por favor, que no hagas alteraciones hasta que concluyamos con la migración, tales como cambio de claves o uso de FTP." \
                   "\n\nNo poseemos una estimativa de tiempo para finalizar el proceso, de todas maneras enviaremos una notificación así que finalicemos." \
                   "\n\nTe avisaremos en breve." \
                   "\n\nSi tienes alguna duda estamos a disposición!" \
                   "\n\nFuerte abrazo!"
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def info_started(self, info_list):
        try:
            self.info_list = info_list
            return "Starting migration..." \
                   "\n\nthread_id: {}" \
                   "\n\nsrc_type: {}" \
                   "\n\nsrc_server: {}" \
                   "\n\ndst_type: {}" \
                   "\n\ndst_server: {}" \
                   "\n\nmain_domain: {}" \
                   "\n\nrequest_type: {}".format(self.info_list[0], self.info_list[1], self.info_list[2], self.info_list[3], self.info_list[4], self.info_list[5], self.info_list[6])

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def info_completed(self, info_list, this_owner=None):
        try:
            self.this_owner = this_owner
            self.info_list = info_list
            if self.this_owner:
                return "INFO: User migration completed." \
                       "\n\nthread_id: {}" \
                       "\n\nowner: {}" \
                       "\n\nmain_domain: {}" \
                       "\n\nuser: {}".format(self.info_list[0], self.this_owner, self.info_list[1], self.info_list[2])
            else:
                return "INFO: User migration completed." \
                       "\n\nthread_id: {}" \
                       "\n\nowner: {}" \
                       "\n\nmain_domain: {}" \
                       "\n\nuser: {}".format(self.info_list[0], self.info_list[1], self.info_list[2], self.info_list[3])

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def info_failed(self, info_list):
        try:
            self.info_list = info_list
            return "ERROR: User migration failed." \
                   "\n\nthread_id: {}" \
                   "\n\nowner: {}" \
                   "\n\nmain_domain: {}" \
                   "\n\nuser: {}".format(self.info_list[0], self.info_list[1], self.info_list[2], self.info_list[3])

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

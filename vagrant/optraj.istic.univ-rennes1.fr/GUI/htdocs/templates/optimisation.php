<link rel="stylesheet" href="css/styleOpti.css" />
<script src="js/login/logadmin.js"></script>
<!-- Pour rendre le header du tableau flottant -->
<script src="js/util/underscore.js"></script>
<script src="js/util/jquery.floatThead.js"></script> 

<div id="optiWindow">
	<!-- le tableau d'affichage des affectations -->
	<table id="tab_site" style="table-layout:auto;width:100%">
	<thead class="thead" id="theader">
		<tr id="tab_site_head_0">
			<th colspan="3">
		  	<div class="form-group input-group" style="margin-bottom:0px;">
		        <span class="input-group-addon"><i class="fa fa-search"></i></span><input type="text" class="form-control" name="search" id="search" autocomplete="off">
			</div>
			</th>					
		</tr>
		<tr id="tab_site_head_1" class="months">
			<th rowspan="2" class="workerInfo" style="width:130px" onclick="sortTable('workerName');" bgcolor="#c1c1c1">Nom</th>
			<th rowspan="2" class="workerInfo" style="width:50px"  onclick="sortTable('workerQualif');" bgcolor="#c1c1c1">Qualif</th>
			<th rowspan="2" class="workerInfo" style="width:100px" onclick="sortTable('workerAddress');" bgcolor="#c1c1c1">Adresse</th>
		</tr>
		<tr id="tab_site_head_2" class="weekNumber"></tr>
	</thead>
	<tbody name="tabContent" id="tab_Workers">
		<tr><td><i style="margin:10px;" class="fa fa-spinner fa-spin fa-lg"></i></td></tr>
	</tbody>
	</table>
	<div id="testAssign"></div>	
</div>

<!-- Modal -->
<div class="modal fade" id="validateModal1" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">Validation des données</h4>
            </div>
            <div class="modal-body">
                Des propositions générée automatiquement n'ont pas été validées manuellement.</br>
                Souhaitez vous valider tout le tableau (propositions incluses) ou uniquement ce que vous avez validé?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                <button type="button" class="btn btn-primary" onclick="validateModifs();">Valider mes modifications</button>
                <button type="button" class="btn btn-primary" onclick="validateAll();">Tout valider</button>
            </div>
        </div>
        <!-- /.modal-content -->
    </div>
    <!-- /.modal-dialog -->
</div>
<!-- ./Modal -->

<!-- Modal -->
<div class="modal fade" id="validateModal2" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel2">Validation des données</h4>
            </div>
            <div class="modal-body">
                Vous allez valider l'ensemble des modifications apportées, êtes vous sûrs ?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Non</button>
                <button type="button" class="btn btn-primary" onclick="validateAll();">Oui</button>
            </div>
        </div>
        <!-- /.modal-content -->
    </div>
    <!-- /.modal-dialog -->
</div>
<!-- ./Modal -->


<script type="text/javascript" src="js/util/dates.js"></script>
<script type="text/javascript" src="js/optimisation/caseManager.js"></script>
<script type="text/javascript" src="js/optimisation/showAffect.js"></script>
<script src="js/optimisation/afterLoad.js" async></script>

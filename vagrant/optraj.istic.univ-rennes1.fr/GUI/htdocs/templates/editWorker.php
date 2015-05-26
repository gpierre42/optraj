<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script src="js/login/logadmin.js"></script>


<div class="panel panel-default" id="createWorker">

	<div class="panel-heading">
		<div id="return">
			<a href="index.php?choix=6"><button name="return" type="button" class="btn btn-default">Retour à la liste</button></a>
	    </div>
    </div>
	<div class="panel-body">
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formNom" class="form-group">
				    <label class="col-sm-5 control-label">Nom</label>
				    <div class="col-sm-7">
						<p id="name" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formPrenom" class="form-group">
				    <label class="col-sm-5 control-label">Prénom</label>
				    <div class="col-sm-7">
				      <p id="firstName" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formDateN" class="form-group">
				    <label class="col-sm-5 control-label">Date de naissance</label>
				    <div class="col-sm-7">
						<p id="birthday" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formCraft" class="form-group">
				    <label class="col-sm-5 control-label">Choissisez un métier</label>
				    <div class="col-sm-7">
				    	<p id="craft" class="formD" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formQualif" class="form-group">
				    <label class="col-sm-5 control-label">Choissisez une qualification</label>
				    <div class="col-sm-7">
				    	<p id="qualification" class="formD" style="margin:7px"></p>
				    </div>
				  </div>
				  <div class="form-group">
				    <label class="col-sm-5 control-label">Adresse</label>
				    <div class="col-sm-7">
				    	<p id="address" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div class="form-group">
				  	<div class="col-sm-6"></div>
				  	<div class="btn-group">
				    	<button type="button" disabled="disabled" class="btn btn-default " id='buttonPlus'><i class="fa fa-exclamation-triangle"></i></button>
					    <button type="button" class="btn btn-info disabled" data-container="body" data-toggle="popover" data-placement="bottom" onclick="checkAddress();" id="cAddress">Vérifier l'adresse</button>
				  	</div>
				  </div>
				  <div class="form-group">
				  	<div class="col-sm-1"></div>
				    <button type="button" class="btn btn-primary disabled" data-container="body" data-toggle="popover" data-placement="right" onclick="editWorker();" id="cValid" data-target="#myModal">Valider les changements</button>
				  </div>
				  <div class="form-group">
					  <div class="col-sm-1"></div>
					  <button type="button" class="btn btn-danger disabled" id="cSuppr" data-toggle="modal" data-target="#supprModal"><i class="fa fa-trash-o"></i>&nbsp; Supprimer l'Ouvrier &nbsp;</button>
				  
				    
                    <!-- Modal -->
                    <div class="modal fade" id="supprModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                        <div class="modal-dialog modal-sm">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">Suppression Ouvrier</h4>
                                </div>
                                <div class="modal-body">
                                    Vous êtes sur le point de supprimer cet ouvrier.<br/>En êtes vous sûr ?
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                                    <button type="button" class="btn btn-primary" onclick="deleteWorker();">Oui</button>
                                </div>
                            </div>
                            <!-- /.modal-content -->
                        </div>
                        <!-- /.modal-dialog -->
                    </div>
                    <!-- /.modal -->
				  </div>
				</form>
			</div>
			<div class="col-md-1"></div>
			<div class="col-md-5" id="map" style="width:400px;height:370px;position:relative;">
				
			</div>
		</div>
		<table id="tabWeek">
		<thead>
			<th>N° semaine</th>
			<th>Nom du chantier</td>
		</thead>
		<tbody id="affectTable"></tbody>
	</table>
	</div>
</div>

<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script type="text/javascript" src="js/minimap.js"></script>
<script type="text/javascript" src="js/util/splitDate.js"></script>
<script type="text/javascript" src="js/util/dates.js"></script>
<script type="text/javascript" src="js/bootstrap/moment.js"></script>
<script type="text/javascript" src="js/bootstrap/bootstrap-datetimepicker.min.js"></script>
<script type="text/javascript" src="js/bootstrap/locales/bootstrap-datetimepicker.fr.js"></script>
<script type="text/javascript" src="js/workers/editWorker.js"></script>

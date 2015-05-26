<div class="panel panel-default" id="editSite">

	<div class="panel-heading">
		<div class="row">
			<div id="return" class="col-md-1">
				<a href="index.php?choix=12"><button name="return" type="button" class="btn btn-default">Retour à la liste</button></a>
		    </div>
		    <div class="col-md-9"></div>
		    <div class="col-sm-2" id="expandMap">
				    <button type="button" class="btn btn-primary" data-container="body" data-toggle="popover" data-placement="right" onclick="expandMap();">Détails navettes</button>
			</div>
		</div>
    </div>
	<div id="panel1" class="panel-body">
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formNum" class="form-group">
				    <label class="col-sm-5 control-label">Numéro du chantier</label>
				    <div class="col-sm-7">
						<p id="numSite" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formNom" class="form-group">
				    <label class="col-sm-5 control-label">Nom du chantier</label>
				    <div class="col-sm-7">
				      <p id="name" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formDateD" class="form-group">
				    <label class="col-sm-5 control-label">Date de début</label>
				    <div class="col-sm-7">
				      <p id="dateInit" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formDateF" class="form-group">
				    <label class="col-sm-5 control-label">Date de fin</label>
				    <div class="col-sm-7">
				      <p id="dateEnd" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formChefC" class="form-group">
				    <label class="col-sm-5 control-label">Chef de chantier</label>
				    <div class="col-sm-7">
				      <p id="siteMaster" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formCondT" class="form-group">
				    <label class="col-sm-5 control-label">Conducteur de travaux</label>
				    <div class="col-sm-7">
				      <p id="siteManager" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formColor" class="form-group">
				    <label class="col-sm-5 control-label">Couleur associée</label>
				    <div class="col-sm-7 form" id="color">
				    	<input class="form-control" id="colorPick" class="color"/>
				    </div>
				    <div class="col-sm-7 bfh-colorpicker" id="colorPicker"></div>
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
				    <button type="button" class="btn btn-primary disabled" data-container="body" data-toggle="popover" data-placement="right" onclick="editSite();" id="cValid" data-target="#myModal">Valider les changements</button>
				  </div>
				  <div class="form-group">
					  <div class="col-sm-1"></div>
					  <button type="button" class="btn btn-danger disabled" id="cSuppr" data-toggle="modal" data-target="#supprModal"><i class="fa fa-trash-o"></i>&nbsp; Supprimer le Chantier</button>
				  
				    
                    <!-- Modal -->
                    <div class="modal fade" id="supprModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                        <div class="modal-dialog modal-sm">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">Suppression Chantier</h4>
                                </div>
                                <div class="modal-body">
                                    Vous êtes sur le point de supprimer ce chantier.<br/>En êtes vous sûr ?
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                                    <button type="button" class="btn btn-primary" onclick="deleteSite();">Oui</button>
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
			<div class="col-md-6">
				<div id="map" style="width:400px;height:370px;position:relative;">
				</div>
			</div>
		</div>
		<table id="tabWeek">
			<thead class="thead">
				<tr id="tabWeek_head_0">
					<th rowspan="3" class="craft" width="200px" bgcolor="#c1c1c1">Metiers</th>
				</tr>
				<tr id="tabWeek_head_1" class="months">
				</tr>
				<tr id="tabWeek_head_2" class="weekNumber"></tr>
			</thead>
			<tbody name="tabContent" id="tab_Week"></tbody>
		</table>
	</div>
</div>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script src="js/util/splitDate.js"></script>
<script src="js/login/logadmin.js"></script>
<script type="text/javascript" src="js/util/dates.js"></script>
<script type="text/javascript" src="js/util/headerTabMonth.js"></script>
<script type="text/javascript" src="js/sites/needOfSite.js"></script>
<script type="text/javascript" src="js/sites/ShuttleModManager.js"></script>
<script type="text/javascript" src="js/sites/minimapSites.js"></script>
<script type="text/javascript" src="js/sites/editSite.js"></script>
<script type="text/javascript" src="js/bootstrap/moment.js"></script>
<script type="text/javascript" src="js/bootstrap/bootstrap-datetimepicker.min.js"></script>
<script type="text/javascript" src="js/bootstrap/locales/bootstrap-datetimepicker.fr.js"></script>
<script type="text/javascript" src="js/bootstrap/bootstrap-multiselect.js"></script>
<script type="text/javascript" src="js/util/jscolor/jscolor.js"></script>
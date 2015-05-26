<div class="panel panel-default" id="createSite">

	<div class="panel-heading">
    </div>
	<div class="panel-body">
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formNum" class="form-group">
				    <label class="col-sm-5 control-label">Numéro du chantier</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="numSite" required placeholder="Ex : 14008RENN">
				    </div>
				  </div>
				  <div id="formNom" class="form-group">
				    <label class="col-sm-5 control-label">Nom du chantier</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="name" required placeholder="Nom du chantier">
				    </div>
				  </div>
				  <div id="formDateD" class="form-group">
				    <label class="col-sm-5 control-label">Date de début</label>
				    <div class="col-sm-7">
					    <div class="input-group date" id='datetimepickerD'>
					      <input class="form-control" name="dateInit" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" />
						  <span class="input-group-addon">
						  	<span class="fa fa-calendar"></span>
						  </span>
					    </div>
				    </div>
				    <script type="text/javascript">
			            $(function () {
			                $('#datetimepickerD').datetimepicker({
			                	language: 'fr',
			                    pickTime: false
			                });
			            });
			        </script>
				  </div>
				  <div id="formDateF" class="form-group">
				    <label class="col-sm-5 control-label">Date de fin</label>
				    <div class="col-sm-7">
					    <div class="input-group date" id='datetimepickerF'>
					      <input class="form-control" name="dateEnd" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" />
						  <span class="input-group-addon">
						  	<span class="fa fa-calendar"></span>
						  </span>
					    </div>
				    </div>
				    <script type="text/javascript">
			            $(function () {
			                $('#datetimepickerF').datetimepicker({
			                	language: 'fr',
			                    pickTime: false
			                });
			            });
			        </script>
				  </div>
				  <div id="formChefC" class="form-group">
				    <label class="col-sm-5 control-label">Chef de chantier</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="siteMaster" required placeholder="Chef de chantier">
				    </div>
				  </div>
				  <div id="formCondT" class="form-group">
				    <label class="col-sm-5 control-label">Conducteur de travaux</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="siteManager" required placeholder="Conducteur de travaux">
				    </div>
				  </div>
				  <div id="formColor" class="form-group">
				    <label class="col-sm-5 control-label">Couleur associée</label>
				    <div id="colorPicker" class="col-sm-7 bfh-colorpicker" data-color="#ff0000"></div>
				  </div>
				  <div class="form-group">
				    <label class="col-sm-5 control-label">Adresse</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="address" id="address" required placeholder="adresse">
				    </div>
				  </div>
				  <div class="form-group">
				  	<div class="col-sm-6"></div>
				  	<div class="btn-group">
				    	<button type="button" disabled="disabled" class="btn btn-default " id='buttonPlus'><i class="fa fa-exclamation-triangle"></i></button>
					    <button type="button" class="btn btn-info" data-container="body" data-toggle="popover" data-placement="bottom" onclick="checkAddress();" id="cAddress">Vérifier l'adresse</button>
				  	</div>
				  </div>
				  <div class="form-group">
				  	<div class="col-sm-1"></div>
				    <button type="button" class="btn btn-primary" data-container="body" data-toggle="popover" data-placement="right" onclick="createSite();" id="cWorker" data-target="#myModal">Créer</button>
				  </div>
				</form>
			</div>
			<div>
				<div class="col-md-5 col-md-offset-1" id="map" style="width:400px;height:370px;position:relative;">
				</div>
			</div>
		</div>
		<button type="button" id="addNeedButton" class="btn btn-default" onclick="showMeTab();">Ajouter vos besoins pour ce chantier</button>

		<table id="tabWeek">
			<thead class="thead">
				<tr id="tab_site_head_0">
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
<script type="text/javascript" src="js/minimap.js"></script>
<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script type="text/javascript" src="js/util/splitDate.js"></script>
<script type="text/javascript" src="js/util/dates.js"></script>
<script type="text/javascript" src="js/util/headerTabMonth.js"></script>
<script type="text/javascript" src="js/login/logadminreq.js"></script>
<script type="text/javascript" src="js/sites/needOfSite.js"></script>
<script type="text/javascript" src="js/bootstrap/moment.js"></script>
<script type="text/javascript" src="js/bootstrap/bootstrap-datetimepicker.min.js"></script>
<script type="text/javascript" src="js/bootstrap/locales/bootstrap-datetimepicker.fr.js"></script>
<script type="text/javascript" src="js/sites/createSite.js"></script>
<div class="panel panel-default" id="createWorker">

	<div class="panel-heading">
    </div>
	<div class="panel-body">
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formNom" class="form-group">
				    <label class="col-sm-5 control-label">Nom</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="name" required placeholder="Nom de l'ouvrier">
				    </div>
				  </div>
				  <div id="formPrenom" class="form-group">
				    <label class="col-sm-5 control-label">Prénom</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="firstName" required placeholder="Prénom de l'ouvrier">
				    </div>
				  </div>
				  <div id="formDateN" class="form-group">
				    <label class="col-sm-5 control-label">Date de naissance</label>
				    <div class="col-sm-7">
					    <div class="input-group date" id='datetimepickerN'>
					      <input class="form-control" name="birthdate" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" />
						  <span class="input-group-addon">
						  	<span class="fa fa-calendar"></span>
						  </span>
					    </div>
				    </div>
				    <script type="text/javascript">
			            $(function () {
			                $('#datetimepickerN').datetimepicker({
			                	language: 'fr',
			                    pickTime: false
			                });
			            });
			        </script>
				  </div>
				  <div id="formCraft" class="form-group">
				    <label class="col-sm-5 control-label">Choissisez un métier</label>
				    <div class="col-sm-7">
				    	<select class="form-control" name="" id="craft_select">
							<option value="">Sélectionner</option>
						</select>
				    </div>
				  </div>
				  <div id="formQualif" class="form-group">
				    <label class="col-sm-5 control-label">Choissisez une qualification</label>
				    <div class="col-sm-7">
				    	<select class="form-control" name="" id="qualif_select">
							<option value="">Sélectionner</option>
						</select>
				    </div>
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
				    	<button type="button" disabled="disabled"
					    	class="btn btn-default " id='buttonPlus'>
					    	<i class="fa fa-exclamation-triangle"></i></button>
					    <button type="button" class="btn btn-info"
						    data-container="body" data-toggle="popover"
						    data-placement="bottom" onclick="checkAddress();"
						    id="cAddress">Vérifier l'adresse</button>
				  	</div>
				  </div>
				  <div class="form-group">
				  	<div class="col-sm-1"></div>
				    <button type="button" class="btn btn-primary"
					    data-container="body" data-toggle="popover"
					    data-placement="right" onclick="createWorker();"
					    id="cWorker">Créer</button>
				  </div>
				</form>
			</div>
			<div>
				<div class="col-md-5 col-md-offset-1" id="map" style="width:400px;height:370px;position:relative;">
				</div>
			</div>
		</div>
	</div>
</div>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="js/minimap.js"></script>
<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script type="text/javascript" src="js/login/logadminreq.js"></script>
<script type="text/javascript" src="js/util/splitDate.js"></script>
<script type="text/javascript" src="js/bootstrap/moment.js"></script>
<script type="text/javascript" src="js/bootstrap/bootstrap-datetimepicker.min.js"></script>
<script type="text/javascript" src="js/bootstrap/locales/bootstrap-datetimepicker.fr.js"></script>
<script type="text/javascript" src="js/workers/createWorker.js"></script>
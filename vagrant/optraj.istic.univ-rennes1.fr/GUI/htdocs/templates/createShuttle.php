<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script src="js/login/logadminreq.js"></script>
<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script src="js/util/splitDate.js"></script>
<script type="text/javascript" src="js/shuttle/createShuttle.js"></script>


<div class="panel panel-default" id="createShuttle">

	<div class="panel-heading">
    </div>
	<div class="panel-body">
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formPlate" class="form-group">
				    <label class="col-sm-5 control-label">Numéro d'immatriculation</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="plate" required placeholder="Numéro d'immatriculation">
				    </div>
				  </div>
				  <div id="formModel" class="form-group">
				    <label class="col-sm-5 control-label">Modèle du véhicule</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="model" required placeholder="Ex : Renault Trafic">
				    </div>
				  </div>
				  <div id="formNbplaces" class="form-group">
				    <label class="col-sm-5 control-label">Nombre de places</label>
				    <div class="col-sm-3">
				      <input name="nbPlace" class="form-control" type='text' id='nbPlaces' value=0>
				    </div>
				  </div>
				  <script>
					    $("input[name='nbPlace']").TouchSpin({
					        min: 0,
					        max: 20
					    });
				  </script>
				  	<div class="form-group">
					  	<div class="col-sm-1"></div>
					    <button type="button" class="btn btn-primary"
						    data-container="body" data-toggle="popover"
						    data-placement="right" onclick="createShuttle();"
						    id="cWorker" data-target="#myModal">Créer</button>
				  	</div>
				</form>
			</div>
		</div>
	</div>
</div>

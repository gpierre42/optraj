<link rel="stylesheet" href="css/styleTimeline.css" />
<script src="js/login/logadmin.js"></script>
<div class="panel panel-default" id="pageTimeline">
	<div class="panel-heading">
		<h4>Planning des chantiers</h4>
    </div>

    <div class="panel-body">
    	<div id="table-row" class="row">
		  	<div class="col-md-8">
		        <table id='table' class="table table-bordered" >
		            <thead id="head" style="border:10px black">
		            	<tr style="border:10px">
							<th colspan="0" style="border-color:transparent">
						    		<div class="col-sm-6 btn-group">
								    	<button type="button" class="btn btn-default " id='buttonPlus'><i class="fa fa-caret-left"></i></button>
									    <button type="button" class="btn btn-default " id="curMonth">Ce mois-ci</button>
									    <button type="button" class="btn btn-default" id='buttonMoins'><i class="fa fa-caret-right"></i></button>
									    <input name="number" class="form-control" type='text' id='nbMonth' value=0 min="1" max="12">
									</div>
    						</th>
		            	</tr>
		            </thead>
		            <tfoot id="foot">
		            	<tr id='tabFoot'>
						</tr>
		            </tfoot>
		            <tbody id ='body'>
		                <!-- Tout ce tableau est généré gràca au javascript contenu dans le fichier script.js -->
		                <tr></tr>
		                <tr></tr>
		            </tbody>
		        </table>
		  	</div>
		  	<div class="col-md-4">
			  	<div class="well" id='info-timeline'>
			  	</div>
		  	</div>
    	</div>
    	<div id="table-row" class="row">

    	</div>
<!--
    	<form class="form-inline" role="form">
		  <div class="form-group">
		    <div class="btn-group">
		    	<button type="button" class="btn btn-default " id='buttonPlus'><i class="fa fa-caret-left"></i></button>
			    <button type="button" class="btn btn-default " id="curMonth">Ce mois-ci</button>
			    <button type="button" class="btn btn-default" id='buttonMoins'><i class="fa fa-caret-right"></i></button>
			</div>
		  </div>
		  <div class="form-group">
		  	<label class="control-label" for="inputSuccess4">Input with success</label>
			<input name="demo3" class="form-control" type='text' id='nbMonth' value=0 min="1" max="12" style="width:40px">
		  </div>
		</form>
-->
    </div>
</div>

<!-- Pour rendre le header du tableau flottant -->
<script src="js/util/underscore.js"></script>
<script src="js/util/jquery.floatThead.js"></script>
<script src="js/timeline/scriptTimeline.js"></script>  

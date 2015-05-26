<script src="js/login/logadmin.js"></script>
<script type="text/javascript" src="js/workers/consultWorker.js"></script>


<div class="panel panel-default" id="consult">
	<div class="panel-heading">
        <h4>Liste des Ouvriers</h4>
    </div>

         <!-- Liste des ouvriers -->
    <div class="panel-body">
	    <div class="row">
            <div class="col-md-8">
                <div id='add'>
                    <a class="btn btn-primary" href="index.php?choix=7">Ajouter un ouvrier</a>                
                    <!-- Cet input n'est la que parce que il nous faut changer le focus de la page lors
                    d'une recherche pour éviter le beug du double click sur un chantier pour avoir le détail -->
                    <input id="test" type="text" style="position: absolute; opacity: 0;">
                </div>
            </div>
            <div class="col-md-4">
    		  	<div class="form-group input-group">
    		        <span class="input-group-addon"><i class="fa fa-search"></i>
    		        </span>
    		        <input type="text" class="form-control" name="search" id="search" autocomplete="off">
    			</div>
            </div>
		</div>

    	<div class="table-responsive">
        	<table class="table table-bordered" id="tab_site"></table>
    	</div>
    </div>
</div>

<script src="js/login/removeButton.js"></script>

<script src="js/login/logadmin.js"></script>
<script src="js/util/dates.js"></script>

<div class="panel panel-default" id="consult">
    <div class="panel-heading">
        <h4> Liste des véhicules</h4>
    </div>
    <div class="panel-body">
        <div class="row">
            <div class="col-md-8">
              <div id='add'>
                <a class="btn btn-primary" href="index.php?choix=14">Ajouter un véhicule</a>
              </div>
              <!-- Cet input n'est la que parce que il nous faut changer le focus de la page lors
              d'une recherche pour éviter le beug du double click sur un chantier pour avoir le détail -->
              <input id="test2" type="text" style="position: absolute; opacity: 0;">
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
            <table class="table table-bordered" id="tab_Car"></table>
        </div>
    </div>
</div>

<script src="js/login/removeButton.js"></script>
<script type="text/javascript" src="js/shuttle/consultShuttle.js"></script>

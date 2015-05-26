<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="js/util/addressResolution.js"></script>
<script src="js/login/logadmin.js"></script>
<script src="js/util/splitDate.js"></script>

<div id="editShuttle">
    <div class="panel-heading">
        <div id="return">
            <a href="index.php?choix=3"><button name="return" type="button" class="btn btn-default">Retour à la liste</button></a>
        </div>
    </div>
    <div class="panel-body">
        <div id="table-row" class="row">
            <div class="col-md-6">
                <form class="form-horizontal" role="form" id="form">
                    <form method="post" action="editShuttle.php">
                        <div id="formModel" class="form-group">
                            <label class="col-sm-5 control-label">Marque de votre véhicule</label>
                            <div class="col-sm-7">
                                <p id="model" style="margin:7px"></p>
                            </div>
                        </div>
                        <div id="formPlate" class="form-group">
                            <label class="col-sm-5 control-label">Numéro de la plaque</label>
                            <div class="col-sm-7">
                                <p id="plate" style="margin:7px"></p>
                            </div>
                        </div>
                        <div id="formNbPlace" class="form-group">
                            <label class="col-sm-5 control-label">Nombre de places</label>
                            <div class="col-sm-7">
                                <p id="nbPlace" style="margin:7px"></p>
                            </div>
                        </div>
                        <div id="formDriver" class="form-group">
                            <label class="col-sm-5 control-label">Chauffeur actuel</label>
                            <div class="col-sm-7">
                                <p id="driver" style="margin:7px"></p>
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="col-sm-1"></div>
                            <button type="button" class="btn btn-danger disabled" id="cSuppr"
                                data-toggle="modal" data-target="#supprModal">
                                <i class="fa fa-trash-o"></i>&nbsp; Supprimer le véhicule</button>


                            <!-- Modal -->
                            <div class="modal fade" id="supprModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-sm">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                            <h4 class="modal-title" id="myModalLabel">Suppression Véhicule</h4>
                                        </div>
                                        <div class="modal-body">
                                            Vous êtes sur le point de supprimer ce véhicule.<br/>En êtes vous sûr ?
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                                            <button type="button" class="btn btn-primary" onclick="deleteCar();">Oui</button>
                                        </div>
                                    </div>
                                    <!-- /.modal-content -->
                                </div>
                                <!-- /.modal-dialog -->
                            </div>
                            <!-- /.modal -->

                        </div>
                    </form>
                    <!-- test -->
                </form>
            </div>
            <div class="col-md-6" id="mapTd">
                <!-- la minicarte pour la vérification d'adresse -->
                <div id="map" style="width:300px;height:300px;"><!-- 
                    <script src="js/minimap.js"></script> -->
                </div>
            </div>
        </div>
    </div>
</div>
<script src="js/login/removeButton.js"></script>
<script type="text/javascript" src="js/shuttle/editShuttle.js"></script>
<script src="js/login/logadminup.js"></script>
<script type="text/javascript" src="js/login/MD5.js"></script>

<div class="panel panel-default" id="editUser">
	<div class="panel-heading">
		<h2> Modification d'un Utilisateur</h2>
    </div>
	<div class="panel-body">
		<div class="row">
			<div class="col-md-8">
				<div id="return">
					<a href="index.php?choix=18"><input type="button" class="btn btn-primary" name="return" value="Retour à la liste"/></a>
				</div>
			</div><br></br>
		</div>
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formLastname" class="form-group">
				    <label class="col-sm-5 control-label">Nom</label>
				    <div class="col-sm-7">
						<p id="name" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formFirstname" class="form-group">
				    <label class="col-sm-5 control-label">Prénom</label>
				    <div class="col-sm-7">
				      <p id="firstname" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formLogin" class="form-group">
				    <label class="col-sm-5 control-label">Login</label>
				    <div class="col-sm-7">
				      <p id="login" class="form" style="margin:7px"></p>
				    </div>
				  </div>
				  <div id="formLevel" class="form-group">
				    <label class="col-sm-5 control-label">Droits</label>
				    <div class="col-sm-7">
				    	<select name="" id="lvladmin_select" class="form">
							<option value="">Sélectionner</option>
							<option value="3">Administration</option>
							<option value="1">Lecture et écriture</option>
							<option value="2">Lecture seule</option>
						</select>
				    </div>
				  </div>
				<!-- Boutons -->
				<div class="form-group">
					<div class="col-sm-1"></div>
					<div class="col-sm-4">
						<button type="button" class="btn btn-primary" data-container="body"
					    	data-toggle="popover" data-placement="right" onclick="editUser();"
					    	id="btnValidate" data-target="#myModal">Valider les changements</button>
					</div>
					<div class="col-sm-1"></div>
					<div class="col-sm-4">
						<a href="index.php?choix=20">
			    		<button type="button" class="btn btn-primary"
				    		data-container="body" data-toggle="popover" data-placement="right"
				    		id="btnEditPassword" data-target="#myModal">Modification du mot de passe</button>
				    	</a>
				    </div>
			    </div>
			    <div class="form-group">
				    <div class="col-sm-1"></div>
				    <div class="col-sm-4">
						<button type="button" class="btn btn-danger" id="btnRemove" data-toggle="modal" data-target="#supprModal">
							<i class="fa fa-trash-o"></i>&nbsp; Supprimer l'Utilisateur &nbsp;</button>
					</div>
                </div>

				<!-- Modal Suppression-->
                <div class="modal fade" id="supprModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-sm">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h4 class="modal-title" id="myModalLabel">Suppression Utilisateur</h4>
                            </div>
                            <div class="modal-body">
                                Vous êtes sur le point de supprimer cet utilisateur.<br/>En êtes vous sûr ?
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                                <button type="button" class="btn btn-primary" onclick="deleteUser();">Oui</button>
                            </div>
                        </div>
                    </div>
                </div>

				</form>
			</div>
			</div>
		</div>
	</div>
</div>
<script type="text/javascript" src="js/login/editUser.js"></script>
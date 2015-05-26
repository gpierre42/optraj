<script src="js/login/logadminup.js"></script>
<script src="js/login/createAdmin.js"></script>
<script type="text/javascript" src="js/login/MD5.js"></script>

<div class="panel panel-default" id="createAdmin">
	<div class="panel-heading">
		<h2> Création d'un utilisateur</h2>
    </div>
	<div class="panel-body">
		<div class="row">
			<div class="col-md-8">
				<div id="return">
					<a href="index.php?choix=18"><input type="button" class="btn btn-primary"name="return" value="Retour à la liste"/></a>
				</div>
			</div><br></br>
		</div>
		<div id="table-row" class="row">
			<div class="col-md-6">
				<form class="form-horizontal" role="form" id="form">
				  <div id="formLastname" class="form-group">
				    <label class="col-sm-5 control-label">Nom</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="name" required placeholder="Nom de l'admistrateur" autocomplete="off">
				    </div>
				  </div>
				  <div id="formFirstname" class="form-group">
				    <label class="col-sm-5 control-label">Prénom</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="firstname" required placeholder="Prénom de l'admistrateur" autocomplete="off">
				    </div>
				  </div>
				  <div id="formLogin" class="form-group">
				    <label class="col-sm-5 control-label">Login</label>
				    <div class="col-sm-7">
				      <input class="form-control" name="login" required placeholder="Login de l'admistrateur" autocomplete="off">
				    </div>
				  </div>
				  <div id="formPassword" class="form-group">
				    <label class="col-sm-5 control-label">Mot de passe</label>
				    <div class="col-sm-7">
				      <input type="password" class="form-control" name="pwd" required placeholder="Mot de passe de l'admistrateur" autocomplete="off">
				    </div>
				  </div>
				  <div id="formLevel" class="form-group">
				    <label class="col-sm-5 control-label">Niveau d'administration : </label>
				    <div class="col-sm-7">
				    	<select name="" id="lvladmin_select">
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
				    <button type="button" class="btn btn-primary" data-container="body"
					    data-toggle="popover" data-placement="right" onclick="createAdmin();"
					    id="cUser">Créer</button>
				  </div>
				</form>
			</div>
			<div class="col-md-1"></div>
		</div>
	</div>
</div>

<script src="js/login/logadminup.js"></script>
<script type="text/javascript" src="js/login/MD5.js"></script>

<div class="panel panel-default">
	<div class="panel-heading">
		<h2> Modification du mot de passe</h2>
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
				  
				  <div id="formNewPwd" class="form-group">
				    <label class="col-sm-5 control-label">Nouveau mot de passe</label>
				    <div class="col-sm-7">
				      <input type="password" class="form-control" id="pwd" name="newpwd" required placeholder="Mot de passe de l'utilisateur" autocomplete="off">
				    </div>
				  </div>
				   <div id="formNewPwdVerif" class="form-group">
				    <label class="col-sm-5 control-label">Répétez le mot de passe</label>
				    <div class="col-sm-7">
				      <input type="password" class="form-control" name="newpwdverif" required placeholder="Répétez le mot de passe" autocomplete="off">
				    </div>
				  </div>
				  
				  <div class="form-group">
				  	<div class="col-sm-1"></div>
				    <button type="button" class="btn btn-primary" data-container="body"
					    data-toggle="popover" data-placement="right" onclick="editPassword();"
					    id="btnValidate" data-target="#myModal">Valider les modifications</button>
				  </div>
				</form>
			</div>
			<div class="col-md-1"></div>
		</div>
	</div>
</div>
<script type="text/javascript" src="js/login/editUser.js"></script>
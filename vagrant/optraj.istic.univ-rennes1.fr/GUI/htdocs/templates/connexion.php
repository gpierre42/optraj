<div class="panel panel-default" id="connexion">
	<div class="panel-heading">
        <h4>Connectez-vous</h4>
    </div>
	<form method="post" action="index.php?choix=14">
		<div class="panel-body">
			<table id="idconnecté">
				<td id="idconnect">
					<div class="panel-body">
                        <form role="form">
                            <fieldset>
                                <div class="form-group">
                                    <input class="form-control" placeholder="Login" id="inputlog" name="login" type="text" autocomplete="off">
                                </div>
                                <div class="form-group">
                                    <input class="form-control" placeholder="Mot de Passe" id="inputpwd" name="pwd" type="password" autocomplete="off" value="">
                                </div>
    							<input type="button" class="btn btn-primary" onclick="checkPwd();" value="Connexion" id="idbutton">
                            </fieldset>
                        </form>
                    </div>
				</td>
			</table>
		</div>
	</form>	
</div>
<script type="text/javascript" src="js/login/login.js"></script>
<script type="text/javascript" src="js/login/MD5.js"></script>



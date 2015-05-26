<!DOCTYPE HTML>
<script src="js/bootstrap/jquery-1.10.2.js"></script>
<script type="text/javascript" src="js/fonctionsIndex.js"></script>
<script src="js/bootstrap/bootstrap-formhelpers.min.js"></script>
<!-- Core Scripts - Include with every page -->
<script src="js/bootstrap/bootstrap.min.js"></script>
<script src="js/bootstrap/plugins/metisMenu/jquery.metisMenu.js"></script>

<!-- SB Admin Scripts - Include with every page -->
<script src="js/bootstrap/sb-admin.js"></script>
<script src="js/util/floatingMenu.js"></script>
<script src="bootstrap-touchspin/bootstrap.touchspin.js"></script>
<script src="js/util/automaticReports.js"></script>
<script src="js/util/connexionProxy.js"></script>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>OPTRAJ</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css"  href="css/style.css" />
        <link href='http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700,300|Roboto:300' rel='stylesheet' type='text/css'>
		<!--[if IE]>  
			<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>  
		<![endif]-->
		<link href="css/bootstrap/bootstrap-formhelpers.min.css" rel="stylesheet">
	    <!-- Core CSS - Include with every page -->
	    <link href="css/bootstrap/bootstrap.min.css" rel="stylesheet">
	    <link href="font-awesome/css/font-awesome.css" rel="stylesheet">
	    <!-- SB Admin CSS - Include with every page -->
	    <link href="css/bootstrap/sb-admin.css" rel="stylesheet">
	    <link href="css/bootstrap/bootstrap-datetimepicker.min.css" rel="stylesheet">
		<link rel="stylesheet" href="css/bootstrap/bootstrap-multiselect.css" type="text/css"/>    
		
		<style type="text/css">
			/* Fix Google Maps canvas
			*
			* Wrap your Google Maps embed in a `.google-map-canvas` to reset Bootstrap's
			* global `box-sizing` changes. You may optionally need to reset the `max-width`
			* on images in case you've applied that anywhere else. (That shouldn't be as
			* necessary with Bootstrap 3 though as that behavior is relegated to the
			* `.img-responsive` class.)
			*/
			
			.google-map-canvas,
			.google-map-canvas * { .box-sizing(content-box); }
			
			/* Optional responsive image override */
			img { max-width: none; }
		</style>
    </head>
    <body>
    <div id="wrapper">

        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".sidebar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.php?choix=1">OPTRAJ</a>
            </div>
            <!-- /.navbar-header -->

             <ul class="nav navbar-top-links navbar-right">
                <li class="dropdown">
                    <a id="menuname" class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu">
						<li id="choix15"><a href="index.php?choix=15"><i class="fa fa-sign-out fa-fw"></i> Login</a></li>
						<li id="choix20"><a style="cursor: pointer; cursor: hand;" onclick="deco()"><i class="fa fa-sign-out fa-fw"></i> Logout</a></li>
					</ul>
                    <!-- /.dropdown-user -->
                </li>
                <!-- /.dropdown -->
            </ul>
            <!-- /.navbar-top-links -->

        </nav>
        <!-- /.navbar-static-top -->
		<div class="test">
	        <nav class="navbar-default navbar-static-side navbar-menu" role="navigation">
	            <div class="sidebar-collapse">
	                <ul class="nav" id="side-menu">
	                    <li class="active" id="choix1"><a href="index.php?choix=1"><i class="fa fa-home fa-fw"></i> Accueil </a></li>
	                    <li id="choix11"><a href="index.php?choix=11"><i class="fa fa-calendar fa-fw"></i> Timeline </a></li>
	                    <li id="choix3"><a href="index.php?choix=3"><i class="fa fa-truck fa-fw"></i> Véhicules</a></li>
						<li id="choix4"><a href="index.php?choix=12"><i class="fa fa-building-o fa-fw"></i> Chantiers</a></li>
	                    <li id="choix6"><a href="index.php?choix=6"><i class="fa fa-male fa-fw"></i> Ouvriers</a></li>
	                    <li id="choix5"><a href="index.php?choix=5"><i class="fa fa-lightbulb-o fa-fw"></i> Affectations</a></li>
	                	<li id="choix18"><a href="index.php?choix=18"><i class="fa fa-female fa-fw"></i> Administrateur</a></li>
						<script type="text/javascript" src="js/login/session.js"></script>
                        
                    </ul>
                    <div id="status">
                    </div>
	                <!-- /#side-menu -->
	            </div>

	            <!-- /.sidebar-collapse -->
	        </nav>
	        <!-- /.navbar-static-side -->
		</div>
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12" id="title">
                    <h2 class="page-header"></h2>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <div class="row">
	          <?php
			      // Si un choix a été fait dans le menu
			      if(isset($_GET["choix"]) && $_GET["choix"] != '')
			         {
					  // On regarde quel est le choix et on charge le content en question
				          switch($_GET["choix"])
				          {
				             case 1 : include("templates/carte.php");
				             		  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Accueil</h2>\'</script>';
				                      break;
				             case 3 : include("templates/consultShuttle.php");
                                      echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Véhicules</h2>\'</script>';
                                      break;
                             case 4 : include("templates/editShuttle.php");
                                      echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Véhicules</h2>\'</script>';
				                      break;
				             case 5 : include("templates/optimisation.php");
				             		  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Affectations</h2>\'</script>';
				             		  break;
							 case 6 : include("templates/consultWorker.php");
				             		  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Consultation Ouvriers</h2>\'</script>';
				             		  break;
				             case 7 : include("templates/createWorker.php");
				             		  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Création Ouvriers</h2>\'</script>';
				             		  break;
				             case 8 : include("templates/editWorker.php");
				             		 echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Modification Ouvriers</h2>\'</script>';
				             		  break;
				             case 9 : include("templates/createSite.php");
				             		 echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Création Chantiers</h2>\'</script>';
				             		  break;
				             case 10 : include("templates/editSite.php");
				             		 echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Édition Chantier</h2>\'</script>';
				             		  break;
                             case 11 : include("templates/timeline.php");
                                     echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Timeline</h2>\'</script>';
                                      break;
                             case 12 : include("templates/consultSite.php");
                                     echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Chantiers</h2>\'</script>';
                                      break;
                             case 14 : include("templates/createShuttle.php");
                                      echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Véhicules</h2>\'</script>';
                                      break;
                             case 15 : include("templates/connexion.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Connexion</h2>\'</script>';
				             		  break;
							 case 16 : include("templates/createAdmin.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Administrateur</h2>\'</script>';
				             		  break;
		             		  case 17 : include("templates/mapOpti.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Création des navettes</h2>\'</script>';
				             		  break;
							 case 18 : include("templates/consultAdmin.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Administrateur</h2>\'</script>';
				             		  break;
							 case 19 : include("templates/editUser.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Administrateur</h2>\'</script>';
				             		  break;
							 case 20 : include("templates/editPassword.php");
									  echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Administrateur</h2>\'</script>';
				             		  break;
				             default : include("templates/carte.php");
				             		   echo '<script>document.getElementById("choix1").className="active"</script>';
   				             		   echo '<script>document.getElementById("title").innerHTML=\'<h2 class="page-header">Accueil</h2>\'</script>';
				          }
	
			         }
					// Si aucun choix a été fait, on charge la page principale, qui est "carte.php" si on est loggué, et la page de login sinon
			         else { 
			         		// echo "<script type='text/javascript' src='http://maps.google.com/maps/api/js?sensor=false'></script>";
			         		echo "<script type='text/javascript'>
			         				if (sessionStorage.isco == 1){
			         					window.location.href='index.php?choix=1';
			         				} else {
			         					$('.row').last().load('templates/connexion.php');
		         					}
									</script>";
	         	  	}
			   ?>
			   <div style="margin-top:30px"></div>

	        </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->

    <!-- Modal déconnexion-->
    <div class="modal fade" id="disconnectModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="alert alert-success">
                <p class="lead text-center"><i class="fa fa-check"></i> A bientôt </p>
            </div>
        </div>
    </div>

    <!-- Modal de rapport (utiliser automaticReports.js)-->
    <div class="modal fade" id="reportModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="alert" id="reportModalAlert">
                <p class="lead text-center" id="reportModalMessage"></p>
            </div>
        </div>
    </div>
    <!-- Modal de confirmation (utiliser automaticReports.js)-->
    <div class="modal fade" id="modalCheck" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-sm">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="modalCheckHeader"></h4>
                </div>
                <div class="modal-body" id="modalCheckBody">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
                    <button type="button" class="btn btn-primary" data-dismiss="modal" id="modalCheckButton">Oui</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal-dialog -->
    </div>
    <!-- /.modal -->

     <footer>
     	<nav class="navbar navbar-default navbar-static-bottom" style="margin-bottom: 0">

	        	<p style="margin-top:15px" class="text-center text-info"><small>&copy; Université de Rennes 1</small></p>

        </nav>
      </footer>
    </body>
</html>

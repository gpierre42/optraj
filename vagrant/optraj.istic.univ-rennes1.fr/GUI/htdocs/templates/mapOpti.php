<!-- Affichage de la map -->
<div class="panel panel-default" id="mapOpti">
    <div id="info" class="panel-heading">
        <div class='row'>
            <div class="col-md-10">
                <h4 id="titleH4"></h4>
            </div>
            <div class="col-md-2">
                <a class="btn btn-primary" onClick="completeShuttles();" id="next">Chantier suivant</a>
            </div>
        </div>
    </div>
    <table id="tabShuttle" style="width:100%">
        <thead class="thead">
            <tr id="tabShuttle_head_0">
            </tr>
            <tr id="tabShuttle_head_1" class="months">
            </tr>
            <tr id="tabShuttle_head_2" class="weekNumber"></tr>
        </thead>
        <tbody name="tabContent" id="tab_Week"></tbody>
    </table>
    <div id="bigMap" style="width:100%;height:600px;position:relative;">
    </div>
</div>
<script type="text/javascript" src="js/util/connexionProxy.js"></script>
<script type="text/javascript" src="js/util/headerTabMonth.js"></script>
<script type="text/javascript" src="js/login/removeButton.js"></script>
<script type="text/javascript" src="js/util/dates.js"></script>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="js/optimisation/mapOpti.js"></script>

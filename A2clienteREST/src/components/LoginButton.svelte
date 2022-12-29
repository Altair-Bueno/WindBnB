<script>
    export let domain;
    export let clientId;
    export let redirectUri;
    export let audience;
</script>

<form method="get" action={"https://" + domain + "/authorize"}>
    <!--
        GET https://YOUR_DOMAIN/authorize?
        response_type=code|token&
        client_id=YOUR_CLIENT_ID&
        connection=CONNECTION&
        redirect_uri=https://YOUR_APP/callback&
        state=STATE&
        ADDITIONAL_PARAMETERS
    -->
    <input hidden name="response_type" value="code"/>
    <input hidden name="client_id" value={clientId}/>
    <input hidden name="audience" value={audience} />
    <input hidden name="redirect_uri" value={redirectUri}/>
    <input type="submit" value="Log in" class="btn btn-primary">
</form>

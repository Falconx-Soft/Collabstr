$(document).ready(function() {
    $(document).on('click', '.location-option', function () {
        if(multiple){
            addLocation($(this).text(), $(this).data("id"));
        } else {
            $("#location-input").val($(this).text());
            $("#location-id").val($(this).data("id")).trigger("change");
        }
        $("#location-dropdown-content").hide();
    });

    $(document).on('focus', '#location-input', function () {
        $(this).attr('autocomplete', 'new-password');
    });

    let globalTimeout = null;
    $(document).on('keyup', '#location-input', function () {
        let input = $(this).val();
        $("#location-id").val("").trigger("change");
        if (input.length < 3) {
            $("#location-dropdown-content").hide();
            return;
        }
        if (globalTimeout != null) clearTimeout(globalTimeout);
        globalTimeout = setTimeout(getLocations, 350);
    });

    function getLocations() {
        let input = $('#location-input').val();
        if (input.length < 3) {
            $("#location-dropdown-content").hide();
            return;
        }
        $.ajax({
            url: locationUrl,
            type: 'POST',
            data: {
                'location': input,
                'country': $("#country-input").val(),
                'csrfmiddlewaretoken': token
            },
            success: function (data) {
                console.log(data.error);
                if (!data.hasOwnProperty('error')) {
                    let locations = data.locations;
                    if (locations) {
                        let options = "";
                        for (let i = 0; i < locations.length; i++) {
                            if (locations[i].region_code) {
                                options = options.concat("<div class='location-option' data-id='" + locations[i].id + "'><b>" + locations[i].city + "</b><span class='region-country'> " + locations[i].region_code + ", " + locations[i].country + "</span></div>");
                            } else {
                                options = options.concat("<div class='location-option' data-id='" + locations[i].id + "'><b>" + locations[i].city + "</b><span class='region-country'> " + locations[i].country + "</span></div>");
                            }
                        }
                        $("#location-dropdown-content").html(options).show();
                    }
                }
            }
        });
    }
});
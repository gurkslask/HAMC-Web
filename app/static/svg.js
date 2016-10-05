var s = Snap(746, 159);

var symb = Snap.load( "/static/VS1.svg",  function(f) {
    s.append(f);
});


function pump(ind, name) {
    this.ind = ind;
    this.name =  name;
    //this.x = s.select(this.name).selectAll('circle')[0].attr("cx");
    //Jthis.y = s.select(this.name).selectAll('circle')[0].attr("cy");

    this.pumpOn = function() {
        s.select(this.name).selectAll('path').animate({stroke:"#bada55"},200);
    };

    this.pumpOff = function() {
        s.select(this.name).selectAll('path').animate({stroke:"grey"},200);
    };

    this.checkState = function() {
        if (this.ind == 1) {
            this.pumpOn();
        }
        else {
            this.pumpOff();
        }
    };

    this.setIndOn = function() {
        this.ind = 1;
    };

    this.setIndOff = function() {
        this.ind = 0;
    };

    this.getXAndY = function() {
        this.x = s.select(this.name).selectAll('circle').attr("cx");
        this.y = s.select(this.name).selectAll('circle').attr("cy");
    };

};

function sensor(name, unit) {
    this.name = name;
    this.value = 42;
    this.unit = unit;

    this.updateValue = function() {
        s.select(this.name).selectAll('text')[0].attr({text: this.value + ' ' + this.unit});
        s.select(this.name).selectAll('text')[1].attr({text: this.name});
        //s.select(this.name).selectAll('text').animate({text: this.value}, 200);
    };
};
                                                                                                           


var s = Snap(1200, 1200);

var symb = Snap.load( "/static/VS1.svg",  function(f) {
    t1 = f.select("#tri");
    c1 = f.select("#cirk");
    test = f.select("#CP2")
    s.append(f);
});


function pump(x, y, ind, larm, name) {
    this.ind = ind;
    this.larm = larm;
    this.name =  '#CP2';

    this.pumpOn = function() {
        t1.animate({transform:"r90, s2, t13, -3", fill:"#bada55"}, 1000, mina.easeinout);
        c1.animate({fill:"#FFFFFF"}, 200);
    };

    this.pumpOff = function() {
        //this.x = s.select(this.name).selectAll('circle').attr("cx");
        //this.y = s.select(this.name).selectAll('circle').attr("cy");
        t1.animate({transform:"r0, s2, t9, 9", fill:"#FFFFFF"}, 1000, mina.easeinout);
        c1.animate({fill:"#bada55"}, 200);
        s.select(this.name).selectAll('circle').animate({fill:"red"},200);
        //os.select(this.name).selectAll('path').animate({transform:"r90, t" + this.x + "," + this.y},200);
        //console.log("r90, t" + this.x + "," + this.y);
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

                                                                                                           


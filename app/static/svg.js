var s = Snap(1200, 1200);
var test = "hej2";
var symb = Snap.load( "/static/VS1.svg",  function(f) {
    t1 = f.select("#tri");
    c1 = f.select("#cirk");
    test = f.select("#CP2")
    s.append(f);
});


function pump(x, y, ind, larm, name) {
    this.x = x;
    this.y = y;
    this.ind = ind;
    this.larm = larm;
    this.name =  name;

    this.pumpOn = function() {
        t1.animate({transform:"r90, s2, t13, -3", fill:"#bada55"}, 1000, mina.easeinout);
        c1.animate({fill:"#FFFFFF"}, 200);
        test.animate({fill:"#FFFFFF"}, 200);
    };
    this.pumpOff = function() {
        t1.animate({transform:"r0, s2, t9, 9", fill:"#FFFFFF"}, 1000, mina.easeinout);
        c1.animate({fill:"#bada55"}, 200);
        test.selectAll('circle').animate({fill:"red"}, 200);
        console.log("hejp");
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

};

                                                                                                           


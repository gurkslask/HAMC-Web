var s = Snap(120, 120);

function pump(x, y, ind, larm){
    this.x = x;
    this.y = y;
    this.ind = ind;
    this.larm = larm;

    this.symb = Snap.load( "/static/pump.svg",  function(f) {
        t1 = f.select("#tri");
        c1 = f.select("#cirk");
        s.append(f);
    });


    this.pumpOn = function() {
        t1.animate({transform:"r90, s2, t13, -3", fill:"#bada55"}, 1000, mina.easeinout);
        c1.animate({fill:"#FFFFFF"}, 200);
    };
    this.pumpOff = function() {
        t1.animate({transform:"r0, s2, t9, 9", fill:"#FFFFFF"}, 1000, mina.easeinout);
        c1.animate({fill:"#bada55"}, 200);
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

                                                                                                           


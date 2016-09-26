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
        alert('pumpon');
        t1.animate({transform:"r90, s2, t13, -3", fill:"#bada55"}, 1000, mina.easeinout);
        c1.animate({fill:"#FFFFFF"}, 2000);
    };
    this.pumpOff = function() {
        alert('pumpoff');
        t1.animate({transform:"r0, s2, t9, 9", fill:"#FFFFFF"}, 1000, mina.easeinout);
        c1.animate({fill:"#bada55"}, 2000);
    };
    this.checkState = function() {
        if this.ind then {
            this.pumpOn();
        } else {
            this.pumpOff();
        };
    };
};

                                                                                                           


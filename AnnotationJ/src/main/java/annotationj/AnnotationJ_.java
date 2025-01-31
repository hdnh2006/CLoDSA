/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package annotationj;

import static ij.IJ.Roi;
import ij.ImagePlus;
import ij.gui.EllipseRoi;
import ij.gui.FreehandRoi;
import ij.gui.MessageDialog;
import ij.gui.OvalRoi;
import ij.gui.PolygonRoi;
import ij.gui.Roi;
import ij.gui.RotatedRectRoi;
import ij.io.SaveDialog;
import ij.plugin.frame.RoiManager;
import java.awt.Polygon;
import java.awt.Rectangle;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.logging.Level;
import java.util.logging.Logger;
import net.imagej.ImageJ;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.scijava.command.Command;
import org.scijava.plugin.Parameter;
import org.scijava.plugin.Plugin;

/**
 *
 * @author joheras
 */
@Plugin(type = Command.class, headless = true, menuPath = "Plugins>AnnotationJ")
public class AnnotationJ_ implements Command {

    @Parameter
    private ImagePlus imp;

    @Override
    public void run() {
        PrintWriter writer = null;
        try {
            int width = imp.getWidth();
            int height = imp.getHeight();
            String name = imp.getTitle();
            JSONObject json = new JSONObject();
            json.put("name", name);
            json.put("width", width);
            json.put("height", height);
            JSONArray arrayAnnotations = new JSONArray();
            RoiManager rm = RoiManager.getInstance();
            if (rm == null) {
                rm = new RoiManager();
                return;
            }
            Roi[] rois = rm.getRoisAsArray();
            for (int i = 0; i < rois.length; i++) {
                JSONObject item = generateAnnotation(rois[i]);
                arrayAnnotations.add(item);
            }
            json.put("annotations", arrayAnnotations);
            SaveDialog sd = new SaveDialog("Select path", "annotations", ".txt");
            writer = new PrintWriter(sd.getDirectory() + sd.getFileName(), "UTF-8");
            writer.println(json.toString());
            writer.close();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(AnnotationJ_.class.getName()).log(Level.SEVERE, null, ex);
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(AnnotationJ_.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private JSONObject generateAnnotation(Roi r) {

        JSONObject json = new JSONObject();
        JSONObject jsonFinal = new JSONObject();
        String label = r.getName();
        json.put("label", label);

//        if (r instanceof RotatedRectRoi) {
//            RotatedRectRoi er = (RotatedRectRoi) r;
//            double[] params = er.getParams();
//            json.put("x1", params[0]);
//            json.put("y1", params[1]);
//            json.put("x2", params[2]);
//            json.put("y2", params[3]);
//            json.put("width", params[4]);
//            jsonFinal.put("rotatedRect", json);
//            return jsonFinal;
//        }
//
//        if (r instanceof EllipseRoi) {
//            EllipseRoi er = (EllipseRoi) r;
//            double[] params = er.getParams();
//            json.put("x1", params[0]);
//            json.put("y1", params[1]);
//            json.put("x2", params[2]);
//            json.put("y2", params[3]);
//            json.put("aspectRatio", params[4]);
//            jsonFinal.put("ellipse", json);
//            return jsonFinal;
//
//        }
        if (r instanceof OvalRoi) {
            OvalRoi or = (OvalRoi) r;
            Polygon pol = or.getPolygon();
            Rectangle r1 = pol.getBounds();
            if (r1.width == r1.height) {

                json.put("x", r1.x);
                json.put("y", r1.y);
                json.put("radius", r1.width);
                jsonFinal.put("circle", json);
                return jsonFinal;
            } else {
                int[] xpoints = pol.xpoints;
                int[] ypoints = pol.ypoints;
                JSONArray arrayX = new JSONArray();
                JSONArray arrayY = new JSONArray();
                for (int i = 0; i < xpoints.length; i++) {
                    arrayX.add(xpoints[i]);
                    arrayY.add(ypoints[i]);
                }
                json.put("xpoints", arrayX);
                json.put("ypoints", arrayY);
                jsonFinal.put("polygon", json);
                return jsonFinal;
            }

        }

//        if (r instanceof FreehandRoi) {
//            PolygonRoi pr = (PolygonRoi) r;
//            int[] xpoints = pr.getPolygon().xpoints;
//            int[] ypoints = pr.getPolygon().ypoints;
//            JSONArray arrayX = new JSONArray();
//            JSONArray arrayY = new JSONArray();
//            for (int i = 0; i < xpoints.length; i++) {
//                arrayX.add(xpoints[i]);
//                arrayY.add(ypoints[i]);
//            }
//            json.put("xpoints", arrayX);
//            json.put("ypoints", arrayY);
//            jsonFinal.put("freeHand", json);
//            return jsonFinal;
//
//        }
        if (r instanceof PolygonRoi) {

            PolygonRoi pr = (PolygonRoi) r;
            int[] xpoints = pr.getPolygon().xpoints;
            int[] ypoints = pr.getPolygon().ypoints;
            JSONArray arrayX = new JSONArray();
            JSONArray arrayY = new JSONArray();
            for (int i = 0; i < xpoints.length; i++) {
                arrayX.add(xpoints[i]);
                arrayY.add(ypoints[i]);
            }
            json.put("xpoints", arrayX);
            json.put("ypoints", arrayY);
            jsonFinal.put("polygon", json);
            return jsonFinal;

        }
        // Otherwise, we have a rectangle
        Rectangle r1 = r.getBounds();
        json.put("x", r1.x);
        json.put("y", r1.y);
        json.put("width", r1.width);
        json.put("height", r1.height);
        jsonFinal.put("rectangle", json);
        return jsonFinal;

    }

    public static void main(final String... args) throws Exception {
        // Launch ImageJ as usual.
        final ImageJ ij = new ImageJ();
        ij.launch(args);

    }

}

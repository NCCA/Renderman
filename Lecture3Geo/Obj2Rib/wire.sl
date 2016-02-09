/* $Id: //depot/main/rman/ratdocs/education/RenderMan_Companion/tutorial/ch16/shaders/wire.sl#4 $  (Pixar - RenderMan Division)  $Date: 2001/01/04 $ */
/*
** Copyright (c) 1998 PIXAR.  All rights reserved.  This program or
** documentation contains proprietary confidential information and trade
** secrets of PIXAR.  Reverse engineering of object code is prohibited.
** Use of copyright notice is precautionary and does not imply publication.
**
**                      RESTRICTED RIGHTS NOTICE
**
** Use, duplication, or disclosure by the Government is subject to the
** following restrictions:  For civilian agencies, subparagraphs (a) through
** (d) of the Commercial Computer Software--Restricted Rights clause at
** 52.227-19 of the FAR; and, for units of the Department of Defense, DoD
** Supplement to the FAR, clause 52.227-7013 (c)(1)(ii), Rights in
** Technical Data and Computer Software.
**
** Pixar
** 1001 West Cutting Blvd.
** Richmond, CA  94804
*/
/* thaw
 * Fri Jun 30 14:19:02 PDT 1989
 *
 * equally spaced wires in world space.
 */
#define HALF 0.5

surface wire( float hwidth=0.0075,smult = 1.0,tmult = 1.0;)
  {
    float rim;
    float s_mid,t_mid,mid;
    color C;

    rim = 2*hwidth;

    C = Cs;

    s_mid = length(dPdu)*(HALF - abs(mod(s*smult,1.0) - HALF))/smult;
    t_mid = length(dPdv)*(HALF - abs(mod(t*tmult,1.0) - HALF))/tmult;
    mid = (s_mid > t_mid) ? t_mid : s_mid;
										    
    Oi = 0.0;
    if (mid < hwidth)
      Oi = 1.0;
    else if ( mid < (hwidth+rim))
      Oi = (1.0-smoothstep(0.0,1.0,(mid-hwidth)/rim));

    Ci = Oi * C;
  }

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AmbassadorEquipmentComponent } from './ambassador-equipment.component';

describe('AmbassadorEquipmentComponent', () => {
  let component: AmbassadorEquipmentComponent;
  let fixture: ComponentFixture<AmbassadorEquipmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AmbassadorEquipmentComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AmbassadorEquipmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
